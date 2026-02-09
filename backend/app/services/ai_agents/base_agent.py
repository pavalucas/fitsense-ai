import datetime
import json
import logging
import os
import time
from typing import Any, Dict, Optional, Union

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from opik import track

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAgent:
    """
    Base class for all AI agents in the FitSense system.
    Handles common functionality like client initialization,
    logging, error handling, and Opik tracing.
    """

    def __init__(self, model: str = "gemini-pro"):
        """
        Initialize the agent with Google Gemini client and model selection.
        """
        self.model_name = os.getenv("GEMINI_MODEL", model)

        # Initialize Google GenAI client
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning(
                "GEMINI_API_KEY not found in environment variables. Agent calls will fail."
            )
        else:
            genai.configure(api_key=api_key)

        # Opik is initialized via environment variables (OPIK_API_KEY, OPIK_WORKSPACE)
        # and the @track decorator.

    def _build_system_prompt(self) -> str:
        """
        Construct the system prompt for the agent.
        This MUST be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement _build_system_prompt")

    def _format_user_message(self, user_input: Union[Dict[str, Any], str]) -> str:
        """
        Format the user input into a string message for the LLM.
        Can be overridden or used as is.
        """
        if isinstance(user_input, str):
            return user_input

        def json_serial(obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")

        return json.dumps(user_input, indent=2, default=json_serial)

    def _extract_reasoning(self, response_text: str) -> Any:
        """
        Extract reasoning and content from the response.
        By default, attempts to parse JSON if the prompt requested it,
        otherwise returns the raw text.
        """
        try:
            # Try to find JSON content if it's wrapped in markdown code blocks
            if "```json" in response_text:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                return json.loads(json_str)
            elif "```" in response_text:
                # fallback for generic code block
                content = response_text.split("```")[1].split("```")[0].strip()
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    return content

            # Try parsing the whole text as JSON
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Fallback: Try to find JSON object structure by locating { and }
            try:
                start_index = response_text.find("{")
                end_index = response_text.rfind("}")
                if start_index != -1 and end_index != -1 and end_index > start_index:
                    json_str = response_text[start_index : end_index + 1]
                    return json.loads(json_str)
            except json.JSONDecodeError:
                pass

            # Return as plain text if not JSON
            return response_text

    @track
    def run(
        self,
        user_input: Union[Dict[str, Any], str],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Run the agent with the given input and context.
        """
        start_time = time.time()

        try:
            system_prompt = self._build_system_prompt()
            formatted_message = self._format_user_message(user_input)

            # Add metadata to Opik trace
            if context:
                # This might need adjustment depending on exact Opik SDK version capabilities
                # but generically we want to log context.
                pass

            logger.info(
                f"Running agent {self.__class__.__name__} with model {self.model_name}"
            )

            # Instantiate model with system instruction
            model = genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt,
            )

            # Configure safety settings to avoid blocking standard fitness advice
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            }

            response = model.generate_content(
                formatted_message,
                safety_settings=safety_settings,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=8192,
                    temperature=0.7,
                ),
            )

            # Check if response was blocked or is empty
            if not response.parts:
                if response.prompt_feedback:
                    logger.warning(f"Prompt feedback: {response.prompt_feedback}")
                raise ValueError("Empty response from Gemini (possibly blocked)")

            response_text = response.text

            # Extract reasoning/output
            result = self._extract_reasoning(response_text)

            # Calculate metrics
            latency = time.time() - start_time

            # Extract usage metadata if available
            token_usage = {}
            if response.usage_metadata:
                token_usage = {
                    "input_tokens": response.usage_metadata.prompt_token_count,
                    "output_tokens": response.usage_metadata.candidates_token_count,
                    "total_tokens": response.usage_metadata.total_token_count,
                }

            logger.info(f"Agent finished in {latency:.2f}s. Tokens: {token_usage}")

            return {
                "status": "success",
                "data": result,
                "raw_response": response_text,
                "metadata": {
                    "latency": latency,
                    "token_usage": token_usage,
                    "model": self.model_name,
                    "agent": self.__class__.__name__,
                },
            }

        except Exception as e:
            logger.error(f"Error running agent: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e),
                "metadata": {
                    "latency": time.time() - start_time,
                    "agent": self.__class__.__name__,
                },
            }

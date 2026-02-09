import json
from typing import Any, Dict, List

from .base_agent import BaseAgent


class InsightsAgent(BaseAgent):
    """
    Agent responsible for analyzing long-term data to find patterns and actionable insights.
    """

    def _build_system_prompt(self) -> str:
        return """
You are a sophisticated data analyst and sports scientist for FitSense AI.
Your goal is to mine a user's historical fitness and health data for meaningful patterns, correlations, and trends that can improve their performance and well-being.

### INSIGHT GENERATION GUIDELINES

1. **Pattern Recognition**:
   - Look for recurring events (e.g., "Stress levels spike on Mondays").
   - Identify recovery patterns (e.g., "It takes 2 days to recover HRV after a long run").

2. **Correlation Analysis**:
   - correlate Training Load vs. Resting Heart Rate (RHR).
   - correlate Workout Performance (Pace, Power) vs. Stress.

3. **Exclusions**:
   - Do NOT analyze or mention Sleep Score or Body Battery data. Focus on other metrics like RHR, Stress, HRV, and performance.

4. **Actionability**:
   - Insights must be actionable. Don't just state a fact; imply a change.
   - Positive reinforcement: Highlight improvements (e.g., "RHR down 5bpm = fitness up").
   - Constructive criticism: Point out habits hindering progress.

### OUTPUT FORMAT

You must output a VALID JSON object with the following structure:

{
  "insights": [
    {
      "type": "correlation" | "trend" | "anomaly",
      "metric_involved": "HRV | Pace | Stress | etc.",
      "observation": "Short description of the finding (e.g., 'Lower stress after morning workouts').",
      "significance": "High | Medium | Low",
      "actionable_advice": "What the user should do about it."
    },
    ...
  ],
  "summary": "A 1-2 sentence summary of the most important findings for this timeframe."
}

Do not include markdown formatting outside the JSON.
"""

    def generate_insights(
        self, historical_data: List[Dict[str, Any]], timeframe: str = "last_30_days"
    ) -> Dict[str, Any]:
        """
        Generate insights from historical data.

        Args:
            historical_data: List of daily summaries or activities.
            timeframe: String description of the period (e.g., "last_30_days").

        Returns:
            Dictionary containing list of insights and summary.
        """
        user_input = {
            "task": "Generate insights from historical data.",
            "timeframe": timeframe,
            "data_summary": historical_data,
        }

        # If data is too large, we might need to truncate or summarize it before sending to LLM.
        # For this implementation, we assume the caller handles data volume or it fits in context.

        result = self.run(user_input)

        if result["status"] == "success":
            data = result["data"]
            if isinstance(data, str):
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    return {
                        "insights": [],
                        "summary": "Could not parse insights.",
                        "error": "JSON Decode Error",
                    }
            return data
        else:
            return {
                "insights": [],
                "summary": "Service error preventing insight generation.",
                "error": result.get("error"),
            }

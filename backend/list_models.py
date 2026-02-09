import os

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY not found in environment variables.")
else:
    try:
        genai.configure(api_key=api_key)
        print(f"Listing available models for API key: {api_key[:5]}...{api_key[-4:]}")

        found_any = False
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"- {m.name} (Display Name: {m.display_name})")
                found_any = True

        if not found_any:
            print("No models found that support generateContent.")
            print(
                "Possible reasons: API key permissions, regional restrictions, or project configuration."
            )

    except Exception as e:
        print(f"Error listing models: {e}")

import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to sys.path so we can import app modules
# This assumes the script is run from the project root or backend/ directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

try:
    from app.services.evaluation.evaluator import run_evaluation
except ImportError as e:
    print(f"Error importing evaluation module: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("Initializing FitSense AI Evaluation...")

    # Verify API Keys
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY not found in environment variables.")
        print("Please add it to your .env file or export it.")
        sys.exit(1)

    if not os.getenv("OPIK_API_KEY") and not os.getenv("OPIK_WORKSPACE"):
        print(
            "Warning: OPIK_API_KEY/WORKSPACE not found. Evaluation results might not be logged to the cloud."
        )

    # Run the evaluation
    try:
        results = run_evaluation()
        print("\nEvaluation Summary:")
        # Opik evaluate returns an Experiment object or similar result structure
        # We print a basic confirmation here. Detailed results are in the Opik dashboard.
        print("Evaluation run completed successfully.")
        print("Check your Opik dashboard for detailed traces and metric scores.")
    except Exception as e:
        print(f"Evaluation failed with error: {e}")
        sys.exit(1)

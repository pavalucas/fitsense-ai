import logging
import os
from typing import Any, Dict

import opik
from app.services.ai_agents.adaptation_agent import AdaptationAgent
from app.services.ai_agents.analysis_agent import AnalysisAgent
from app.services.ai_agents.planning_agent import PlanningAgent
from app.services.evaluation.metrics import SafetyMetric, SpecificityMetric, ToneMetric
from app.services.evaluation.test_scenarios import TEST_SCENARIOS
from opik import Opik

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize agents
# We initialize them globally for the evaluation task to access
planning_agent = PlanningAgent()
adaptation_agent = AdaptationAgent()
analysis_agent = AnalysisAgent()


def evaluation_task(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Task function for Opik evaluation.
    Routes the scenario item to the appropriate agent based on 'agent_target'.
    """
    agent_target = item.get("agent_target")
    input_data = item.get("input_data", {})

    logger.info(f"Evaluating scenario: {item.get('name')} ({agent_target})")

    try:
        if agent_target == "planning_agent":
            # PlanningAgent expects: user_profile, recent_workouts, recovery_status
            result = planning_agent.generate_weekly_plan(
                user_profile=input_data.get("user_profile"),
                recent_workouts=input_data.get("recent_workouts", []),
                recovery_status=input_data.get("recovery_status", {}),
            )
        elif agent_target == "adaptation_agent":
            # AdaptationAgent expects: scheduled_workout, today_recovery, recent_training_load
            result = adaptation_agent.adapt_workout(
                scheduled_workout=input_data.get("scheduled_workout"),
                today_recovery=input_data.get("today_recovery"),
                recent_training_load=input_data.get("recent_training_load"),
            )
        elif agent_target == "analysis_agent":
            # AnalysisAgent expects: garmin_data
            result = analysis_agent.analyze_recovery_status(
                garmin_data=input_data.get("garmin_data")
            )
        else:
            raise ValueError(f"Unknown agent target: {agent_target}")

        # Return dict with 'output' key for Opik metrics
        return {"output": result}

    except Exception as e:
        logger.error(f"Error in evaluation task for {item.get('name')}: {e}")
        return {"error": str(e)}


def run_evaluation():
    """
    Run the Opik evaluation suite using the defined scenarios and metrics.
    """
    logger.info("Starting FitSense AI Opik Evaluation...")

    # Define custom metrics that use Gemini as a judge
    metrics = [
        SafetyMetric(),
        SpecificityMetric(),
        ToneMetric(),
    ]

    # Prepare Opik dataset
    try:
        client = Opik()
        # Clean up existing dataset if it exists to avoid duplicates
        try:
            client.delete_dataset(name="FitSense Scenarios")
        except Exception:
            pass

        dataset = client.get_or_create_dataset(name="FitSense Scenarios")

        # Add 'input' key to scenarios for Opik metrics
        scenarios_for_dataset = []
        for scenario in TEST_SCENARIOS:
            item = scenario.copy()
            item["input"] = scenario.get("input_data")
            scenarios_for_dataset.append(item)

        dataset.insert(scenarios_for_dataset)
    except Exception as e:
        logger.error(f"Failed to prepare dataset: {e}")
        raise e

    # Run evaluation
    # opik.evaluate handles the iteration, tracing, and metric calculation
    try:
        results = opik.evaluate(
            experiment_name="FitSense AI Agents Evaluation",
            dataset=dataset,
            task=evaluation_task,
            scoring_metrics=metrics,
            verbose=True,
        )

        logger.info("Evaluation complete.")
        return results

    except Exception as e:
        logger.error(f"Failed to run Opik evaluation: {e}")
        # In case of configuration error (e.g. missing API key), we log it but don't crash the app
        print(f"Evaluation Setup Error: {e}")


if __name__ == "__main__":
    # Check for keys before running
    if not os.getenv("GEMINI_API_KEY"):
        print("Error: GEMINI_API_KEY is not set.")
    elif not os.getenv("OPIK_API_KEY") and not os.getenv("OPIK_WORKSPACE"):
        # Opik might work in local mode without key, but usually needs one for cloud
        print(
            "Warning: OPIK_API_KEY/WORKSPACE not set. Ensure Opik is configured correctly."
        )

    run_evaluation()

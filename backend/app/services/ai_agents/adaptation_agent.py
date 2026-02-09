import json
from typing import Any, Dict

from .base_agent import BaseAgent


class AdaptationAgent(BaseAgent):
    """
    Agent responsible for adapting today's scheduled workout based on real-time recovery metrics.
    """

    def _build_system_prompt(self) -> str:
        return """
You are an expert fitness coach specializing in auto-regulation and recovery management for FitSense AI.
Your goal is to evaluate a user's scheduled workout against their current physiological state and recommend adaptations if necessary.

### ADAPTATION GUIDELINES & DECISION MATRIX

Your primary directive is "Safety First, Consistency Second, Intensity Third".

Analyze the input data using these rules. IMPORTANT: Do NOT use Body Battery or Sleep Score in your decision making. Rely on Stress, Resting Heart Rate (RHR), and Training Load.

1. **Critical Recovery Failure (RED ZONE)**:
   - IF (Stress > 70 AND RHR significantly elevated) OR very high recent acute load:
   - **ACTION**: Change workout to "Rest" or "Active Recovery" (e.g., light walking, stretching, yoga).
   - **INTENSITY**: Low.

2. **Compromised Recovery (YELLOW ZONE)**:
   - IF Stress is elevated (50-70) OR High recent training load:
   - **ACTION**: Maintain the exercise selection but reduce volume (sets/reps) by 30-50% OR reduce intensity/weight.
   - **INTENSITY**: Low to Moderate.

3. **Good Recovery (GREEN ZONE)**:
   - IF Stress is normal (<50) AND RHR is stable:
   - **ACTION**: Proceed with scheduled workout as planned.
   - **INTENSITY**: As scheduled.

4. **Excellent Recovery (Performance Zone)**:
   - IF Stress is low (<30) AND RHR is low/stable:
   - **ACTION**: Consider adding a small challenge (e.g., +5% weight or +1 set) if the user feels good.

### OUTPUT FORMAT

You must output a VALID JSON object with the following structure:

{
  "modification_status": "unchanged" | "modified" | "cancelled_for_rest",
  "adaptation_reason": "Clear explanation of why the change was made (or not) based on metrics.",
  "safety_check": {
    "passed": true | false,
    "concerns": ["List of specific concerns if any, e.g., 'Elevated RHR'"]
  },
  "original_workout_summary": "Brief summary of what was planned",
  "adapted_workout": {
    "workout_type": "...",
    "exercises": [
       { "name": "...", "sets": ..., "reps": ..., "rest": ... }
    ],
    "intensity": "...",
    "estimated_duration": ...
  }
}

If `modification_status` is "unchanged", `adapted_workout` should match the original.
"""

    def adapt_workout(
        self,
        scheduled_workout: Dict[str, Any],
        today_recovery: Dict[str, Any],
        recent_training_load: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Adapt the scheduled workout based on recovery and load.

        Args:
            scheduled_workout: The workout planned for today.
            today_recovery: Detailed recovery metrics (Body Battery, Sleep, Stress, etc.).
            recent_training_load: Summary of recent strain/load.

        Returns:
            Dictionary containing the adaptation decision and the resulting workout.
        """
        user_input = {
            "task": "Adapt scheduled workout based on recovery.",
            "scheduled_workout": scheduled_workout,
            "current_recovery_metrics": today_recovery,
            "recent_training_load": recent_training_load,
        }

        result = self.run(user_input)

        if result["status"] == "success":
            data = result["data"]
            if isinstance(data, str):
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    # Fallback
                    return {
                        "modification_status": "error",
                        "adaptation_reason": "Could not parse agent response.",
                        "safety_check": {
                            "passed": False,
                            "concerns": ["Parsing Error"],
                        },
                        "adapted_workout": scheduled_workout,
                    }
            return data
        else:
            return {
                "modification_status": "error",
                "adaptation_reason": f"Agent error: {result.get('error')}",
                "safety_check": {"passed": False, "concerns": ["Service Error"]},
                "adapted_workout": scheduled_workout,
            }

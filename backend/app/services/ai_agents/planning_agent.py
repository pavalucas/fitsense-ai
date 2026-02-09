import json
from typing import Any, Dict, List

from .base_agent import BaseAgent


class PlanningAgent(BaseAgent):
    """
    Agent responsible for generating weekly workout plans based on user goals and recovery status.
    """

    def _build_system_prompt(self) -> str:
        return """
You are an expert fitness coach and planner for the FitSense AI system.
Your goal is to generate a comprehensive 7-day workout plan tailored to a user's profile, recent history, and current recovery status.

### PLANNING GUIDELINES

1. **User Profile & Goals**:
   - Respect the user's fitness level (Beginner, Intermediate, Advanced).
   - Align the plan with their primary goal (e.g., Weight Loss, Muscle Gain, Endurance, General Health).
   - Consider available equipment (e.g., Gym, Home, Bodyweight).

2. **Exercise Science Principles**:
   - **Progressive Overload**: Gradually increase intensity or volume week over week.
   - **Specificity**: Exercises must match the goal.
   - **Recovery**: Include rest days or active recovery days, especially after intense sessions.
   - **Balance**: Ensure opposing muscle groups are worked (e.g., Push/Pull).

- **Context Awareness**:
- If `recovery_status` is "Poor", reduce intensity/volume for the first few days.
- If `recent_workouts` show high volume, ensure adequate recovery is planned.
- **IMPORTANT**: Do NOT use Sleep Score or Body Battery metrics to determine the plan intensity or volume. Rely on subjective feedback, Stress, and Resting Heart Rate trends instead.

### OUTPUT FORMAT

You must output a VALID JSON object with the following structure:

{
  "week_summary": "Brief overview of the week's focus (e.g., 'Focus on hypertrophy and active recovery').",
  "daily_plans": [
    {
      "day": "Monday",
      "workout_type": "Strength (Upper Body) | Strength (Lower Body) | Cardio | HIIT | Rest | Active Recovery | etc.",
      "focus": "Brief description of the session focus",
      "exercises": [
        {
          "name": "Exercise Name",
          "sets": <int>,
          "reps": "Range (e.g., 8-12) or specific number",
          "rest_seconds": <int>,
          "notes": "Optional technique notes"
        }
      ],
      "estimated_duration": <int (minutes)>,
      "intensity": "Low | Moderate | High"
    },
    ... (Repeat for Tuesday through Sunday)
  ]
}

- For Rest days, `exercises` should be empty or contain simple instructions like "Walk" or "Stretch".
- Ensure there are exactly 7 entries in `daily_plans`.
- Do not include markdown formatting outside the JSON.
"""

    def generate_weekly_plan(
        self,
        user_profile: Dict[str, Any],
        recent_workouts: List[Dict[str, Any]],
        recovery_status: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a 7-day workout plan.

        Args:
            user_profile: Dict containing user goals, level, equipment, etc.
            recent_workouts: List of recent workout dictionaries.
            recovery_status: The output from the AnalysisAgent (recovery assessment).

        Returns:
            Dictionary containing the weekly plan.
        """
        user_input = {
            "task": "Generate a weekly workout plan.",
            "user_profile": user_profile,
            "recent_workouts_summary": recent_workouts,
            "current_recovery_status": recovery_status,
        }

        result = self.run(user_input)

        if result["status"] == "success":
            data = result["data"]
            if isinstance(data, str):
                try:
                    return json.loads(data)
                except json.JSONDecodeError:
                    # Fallback structure if parsing fails
                    return {
                        "week_summary": "Error parsing plan.",
                        "daily_plans": [],
                        "error": "Could not parse JSON response.",
                    }
            return data
        else:
            return {
                "week_summary": "Could not generate plan due to service error.",
                "daily_plans": [],
                "error": result.get("error"),
            }

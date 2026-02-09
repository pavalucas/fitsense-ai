import json
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent


class AnalysisAgent(BaseAgent):
    """
    Agent responsible for analyzing Garmin data to determine recovery status.
    """

    def _build_system_prompt(self) -> str:
        return """
You are an expert sports scientist and recovery analyst for the FitSense AI system.
Your goal is to analyze a user's recent Garmin health and fitness data to determine their current recovery status and readiness for training.

You will receive a JSON object containing recent Garmin data (last 7-14 days), including:
- Daily summaries (Resting Heart Rate, Max Heart Rate, Stress levels, Body Battery)
- Sleep data (Sleep Score, Duration, REM/Deep sleep)
- HRV Status (if available)
- Training history (recent activities)

### ANALYSIS GUIDELINES

1. **Recovery Metric Interpretation**:
   - **Stress**: Lower is better. Avg stress >40 suggests fatigue or illness.
   - **RHR (Resting Heart Rate)**: Sudden increase (>3-5 bpm above baseline) indicates fatigue/illness.
   - **HRV (Heart Rate Variability)**: Significant drop below baseline indicates stress/fatigue.
   - **IMPORTANT**: Do NOT use Body Battery or Sleep Score in your analysis. Rely on Stress, RHR, and HRV.

2. **Pattern Recognition**:
   - Look for trends over the last few days (e.g., rising RHR, dropping HRV).
   - Identify correlations (e.g., hard workout followed by high stress).

3. **Overtraining Signals**:
   - Consistently elevated RHR.
   - Persistently high stress levels.
   - Significant drop in HRV over multiple days.

4. **Decision Rules**:
   - IF Stress > 50 AND RHR elevated THEN Status = "Poor" -> Recommendation: Light activity only.
   - IF RHR is stable and HRV is baseline or higher THEN Status = "Excellent" -> Recommendation: High intensity allowed.
   - Else -> Status = "Moderate" or "Good" depending on mix of metrics.

### OUTPUT FORMAT

You must output a VALID JSON object with the following structure:

{
  "recovery_status": "poor" | "moderate" | "good" | "excellent",
  "recovery_score": <integer 0-100>,
  "key_metrics_summary": {
    "stress_level": "Low/Moderate/High",
    "rhr_trend": "Stable/Elevated/Decreasing",
    "hrv_status": "Balanced/Unbalanced/Low"
  },
  "trends_identified": [
    "List of strings describing specific trends, e.g., 'RHR has been stable for 3 days'",
    "RHR is slightly elevated today compared to weekly average"
  ],
  "recommendation": {
    "action": "Rest" | "Active Recovery" | "Maintenance" | "Train Hard",
    "intensity_level": "Low" | "Moderate" | "High",
    "advice": "Specific advice string..."
  },
  "reasoning": "Detailed explanation of why this assessment was made based on the evidence."
}

Do not include any markdown formatting or explanations outside the JSON object.
"""

    def analyze_recovery_status(self, garmin_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the provided Garmin data to determine recovery status.

        Args:
            garmin_data: Dictionary containing Garmin metrics (daily stats, sleep, etc.)

        Returns:
            Dictionary with analysis results matching the OUTPUT FORMAT schema.
        """
        # Prepare the input for the agent
        # We wrap the data to be explicit about what the agent is looking at
        user_input = {
            "task": "Analyze recovery status based on the following Garmin data.",
            "data": garmin_data,
        }

        result = self.run(user_input)

        if result["status"] == "success":
            # The BaseAgent._extract_reasoning attempts to parse JSON
            # Check if result['data'] is indeed a dict, if not try to parse it
            data = result["data"]
            if isinstance(data, str):
                try:
                    data = json.loads(data)
                except json.JSONDecodeError:
                    # If parsing fails, return a structure indicating failure but preserving raw response
                    return {
                        "recovery_status": "moderate",
                        "recovery_score": 50,
                        "key_metrics_summary": {},
                        "trends_identified": ["JSON parsing failed"],
                        "recommendation": {
                            "action": "Maintenance",
                            "intensity_level": "Moderate",
                            "advice": "Analysis format error. Proceed with caution.",
                        },
                        "reasoning": f"Raw response could not be parsed: {data[:100]}...",
                    }
            return data
        else:
            # Fallback in case of API failure
            return {
                "recovery_status": "moderate",
                "recovery_score": 50,
                "key_metrics_summary": {},
                "trends_identified": ["Analysis service unavailable"],
                "recommendation": {
                    "action": "Maintenance",
                    "intensity_level": "Moderate",
                    "advice": "Could not analyze data due to service error. Listen to your body.",
                },
                "reasoning": f"Agent error: {result.get('error')}",
            }

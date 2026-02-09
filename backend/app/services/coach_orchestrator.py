import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from app.services.ai_agents.adaptation_agent import AdaptationAgent
from app.services.ai_agents.analysis_agent import AnalysisAgent
from app.services.ai_agents.insights_agent import InsightsAgent
from app.services.ai_agents.planning_agent import PlanningAgent
from app.services.garmin_service import GarminService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoachOrchestrator:
    """
    Orchestrator service that coordinates specialized AI agents and Garmin data
    to provide holistic coaching, planning, and insights.
    """

    def __init__(self, garmin_service: GarminService):
        """
        Initialize with a GarminService instance and instantiate all agents.
        """
        self.garmin_service = garmin_service
        self.analysis_agent = AnalysisAgent()
        self.planning_agent = PlanningAgent()
        self.adaptation_agent = AdaptationAgent()
        self.insights_agent = InsightsAgent()

    def _fetch_recent_history(
        self, days: int
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Helper to fetch recent daily summaries and activities.
        Returns: (daily_summaries, activities) as lists of dicts.
        """
        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Fetch activities
        # Using dummy tokens as the service handles auth internally if logged in
        activities_objs = self.garmin_service.get_activities(
            "internal", "internal", start_date, end_date
        )
        activities = [
            act.model_dump() if hasattr(act, "model_dump") else act.__dict__
            for act in activities_objs
        ]

        # Fetch daily summaries
        daily_summaries = []
        current = start_date
        while current <= end_date:
            try:
                summary_obj = self.garmin_service.get_daily_summary(
                    "internal", "internal", current
                )
                summary_dict = (
                    summary_obj.model_dump()
                    if hasattr(summary_obj, "model_dump")
                    else summary_obj.__dict__
                )
                daily_summaries.append(summary_dict)
            except Exception as e:
                logger.warning(f"Could not fetch summary for {current}: {e}")
            current += timedelta(days=1)

        return daily_summaries, activities

    def generate_weekly_plan(self, user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive weekly workout plan.

        1. Analyzes recent recovery and load (last 14 days).
        2. Generates a plan based on user profile and analysis.
        """
        logger.info("Starting weekly plan generation workflow...")

        # 1. Gather Context
        recent_summaries, recent_activities = self._fetch_recent_history(days=14)

        # Prepare data for analysis in a consistent format
        analysis_context = {
            "daily_summaries": recent_summaries,
            "activities": recent_activities,
        }

        # 2. Analyze Recovery Status
        logger.info("Calling AnalysisAgent...")
        recovery_analysis = self.analysis_agent.analyze_recovery_status(
            analysis_context
        )

        # 3. Generate Plan
        logger.info("Calling PlanningAgent...")
        weekly_plan = self.planning_agent.generate_weekly_plan(
            user_profile=user_profile,
            recent_workouts=recent_activities,
            recovery_status=recovery_analysis,
        )

        return {
            "status": "success",
            "recovery_analysis": recovery_analysis,
            "weekly_plan": weekly_plan,
        }

    def get_daily_guidance(
        self, scheduled_workout: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get guidance for today. If a workout is scheduled, adapt it based on recovery.
        """
        logger.info("Generating daily guidance...")

        today = date.today()

        # 1. Get today's recovery metrics
        try:
            todays_data_obj = self.garmin_service.get_daily_summary(
                "internal", "internal", today
            )
            todays_data = (
                todays_data_obj.model_dump()
                if hasattr(todays_data_obj, "model_dump")
                else todays_data_obj.__dict__
            )
        except Exception as e:
            logger.error(f"Failed to fetch today's data: {e}")
            todays_data = {}

        # 2. Analyze Current Status
        # Pass today's data in the same format the agent expects for weekly plans
        analysis_context = {
            "daily_summaries": [todays_data] if todays_data else [],
            "activities": [],
        }
        analysis_result = self.analysis_agent.analyze_recovery_status(analysis_context)

        response = {
            "date": str(today),
            "recovery_status": analysis_result,
            "guidance_type": "general",
        }

        # 3. Adapt Workout (if scheduled)
        if scheduled_workout:
            logger.info("Adapting scheduled workout...")

            # Fetch very recent load (last 7 days) for adaptation context
            _, recent_activities = self._fetch_recent_history(days=7)

            adaptation_result = self.adaptation_agent.adapt_workout(
                scheduled_workout=scheduled_workout,
                today_recovery=todays_data,
                recent_training_load={
                    "recent_activities_count": len(recent_activities)
                },
            )

            response["guidance_type"] = "workout_adaptation"
            response["adaptation"] = adaptation_result

        return response

    def get_insights(self, days_back: int = 30) -> Dict[str, Any]:
        """
        Generate long-term insights based on historical data.
        """
        logger.info(f"Generating insights for last {days_back} days...")

        # 1. Fetch History
        summaries, activities = self._fetch_recent_history(days=days_back)

        # 2. Generate Insights
        insights_context = {"daily_summaries": summaries, "activities": activities}
        insights_result = self.insights_agent.generate_insights(
            historical_data=[insights_context],
            timeframe=f"Last {days_back} days",
        )

        return insights_result

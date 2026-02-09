import logging
from typing import Any, Dict, List, Optional

from app.dependencies import get_coach_orchestrator
from app.services.coach_orchestrator import CoachOrchestrator
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/coach", tags=["Coach"])


# --- Pydantic Models for Request/Response ---


class UserProfile(BaseModel):
    fitness_level: str
    goals: List[str]
    equipment: List[str]
    limitations: List[str] = []


class ScheduledWorkout(BaseModel):
    workout_type: str
    intensity: str
    duration_min: int
    exercises: List[str] = []
    notes: Optional[str] = None


class DailyGuidanceRequest(BaseModel):
    scheduled_workout: Optional[ScheduledWorkout] = None


# --- Endpoints ---


@router.post("/plan")
async def generate_weekly_plan(
    user_profile: UserProfile,
    orchestrator: CoachOrchestrator = Depends(get_coach_orchestrator),
):
    """
    Generate a personalized weekly workout plan based on user profile and recent recovery data.
    """
    try:
        # Convert Pydantic model to dict for the orchestrator
        profile_dict = user_profile.model_dump()
        result = orchestrator.generate_weekly_plan(user_profile=profile_dict)
        return result
    except Exception as e:
        logger.error(f"Error generating weekly plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/daily")
async def get_daily_guidance(
    request: DailyGuidanceRequest,
    orchestrator: CoachOrchestrator = Depends(get_coach_orchestrator),
):
    """
    Get guidance for today based on real-time recovery metrics.
    If a scheduled workout is provided, the AI will adapt it if necessary.
    """
    try:
        # Convert Pydantic model to dict if present
        scheduled_workout_dict = None
        if request.scheduled_workout:
            scheduled_workout_dict = request.scheduled_workout.model_dump()

        result = orchestrator.get_daily_guidance(
            scheduled_workout=scheduled_workout_dict
        )
        return result
    except Exception as e:
        logger.error(f"Error getting daily guidance: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insights")
async def get_insights(
    days: int = 30, orchestrator: CoachOrchestrator = Depends(get_coach_orchestrator)
):
    """
    Generate actionable insights based on historical data.
    """
    try:
        result = orchestrator.get_insights(days_back=days)
        return result
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

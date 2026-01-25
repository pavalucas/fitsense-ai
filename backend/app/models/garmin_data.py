from datetime import date, datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel


class GarminData(BaseModel):
    """
    Pydantic model for daily Garmin health and wellness data.
    Corresponds to Phase 2, Step 2.2 of the dev guide.
    """

    date: date

    # Sleep metrics
    sleep_score: Optional[int] = None
    total_sleep_minutes: Optional[int] = None
    deep_sleep_minutes: Optional[int] = None
    light_sleep_minutes: Optional[int] = None
    rem_sleep_minutes: Optional[int] = None
    awake_minutes: Optional[int] = None

    # Recovery
    body_battery: Optional[int] = None
    stress_score: Optional[int] = None
    resting_heart_rate: Optional[int] = None
    hrv: Optional[int] = None

    # Activity
    steps: Optional[int] = None
    active_minutes: Optional[int] = None
    calories_burned: Optional[int] = None

    # Body composition
    weight_kg: Optional[float] = None
    body_fat_percentage: Optional[float] = None
    muscle_mass_kg: Optional[float] = None

    # Raw data for full Garmin response
    raw_data: Optional[Dict[str, Any]] = None


class GarminActivity(BaseModel):
    """
    Pydantic model for individual Garmin workouts/activities.
    Corresponds to Phase 2, Step 2.2 of the dev guide.
    """

    activity_type: str
    start_time: datetime
    duration_minutes: float

    # Running / Cardio metrics
    distance_km: Optional[float] = None
    avg_pace: Optional[float] = None
    avg_hr: Optional[int] = None
    max_hr: Optional[int] = None
    elevation_gain: Optional[float] = None
    vo2_max: Optional[float] = None

    # Strength metrics
    exercise_count: Optional[int] = None
    set_count: Optional[int] = None

    # Training effect metrics
    aerobic_training_effect: Optional[float] = None
    anaerobic_training_effect: Optional[float] = None

    # Raw data
    raw_data: Optional[Dict[str, Any]] = None

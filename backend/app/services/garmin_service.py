import json
import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional

import garth
from pydantic import ValidationError

# Assuming running from backend/ directory as root, or app installed as package
try:
    from app.models.garmin_data import GarminActivity, GarminData
except ImportError:
    # Fallback for local testing if path setup is different
    import os
    import sys

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
    from app.models.garmin_data import GarminActivity, GarminData

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GarminService:
    """
    Service to handle interactions with Garmin API using 'garth' library.
    Capable of using both mocked data (for testing) and real data (if credentials provided).
    """

    def __init__(
        self,
        email: Optional[str] = None,
        password: Optional[str] = None,
        display_name: Optional[str] = None,
    ):
        self.client = None
        self.is_authenticated = False
        self.display_name = display_name

        if email and password:
            self.login(email, password, display_name)

    def login(self, email: str, password: str, display_name: Optional[str] = None):
        """
        Authenticate with Garmin Connect using email and password.
        Uses garth library which handles the unofficial API authentication.
        """
        try:
            # garth.login handles session creation and saves it globally in garth.client
            garth.login(email, password)
            self.client = garth.client

            if display_name:
                self.display_name = display_name
                logger.info(f"Using provided display name: {self.display_name}")
            else:
                self.display_name = self.client.username
                # If username is an email, try to fetch the actual display name
                if "@" in self.display_name:
                    try:
                        profile = self.client.connectapi(
                            "/userprofile-service/socialProfile"
                        )
                        if profile and "displayName" in profile:
                            self.display_name = profile["displayName"]
                            logger.info(
                                f"Resolved Garmin display name: {self.display_name}"
                            )
                    except Exception as e:
                        logger.warning(f"Could not resolve Garmin display name: {e}")
                        logger.warning(
                            "Please provide GARMIN_DISPLAY_NAME in .env file"
                        )

            self.is_authenticated = True
            logger.info(f"Successfully logged in as {email}")
        except Exception as e:
            logger.error(f"Failed to login to Garmin: {e}")
            raise

    def get_oauth_url(self) -> Dict[str, str]:
        """
        Generate OAuth authorization URL.
        NOTE: This is for the Official Garmin Health API flow.
        Since we are using 'garth' (unofficial API) for direct data access,
        this remains mocked.
        """
        logger.info("Generating mocked OAuth URL (Official API flow)")
        return {
            "url": "https://connect.garmin.com/oauthConfirm?oauth_token=mock_oauth_token",
            "oauth_token": "mock_oauth_token",
            "oauth_token_secret": "mock_oauth_token_secret",
        }

    def exchange_token(self, oauth_token: str, oauth_verifier: str) -> Dict[str, str]:
        """
        Exchange OAuth tokens for access tokens.
        Mocked for Official API flow.
        """
        logger.info(f"Exchanging token {oauth_token} with verifier {oauth_verifier}")
        return {
            "access_token": "mock_access_token",
            "access_token_secret": "mock_access_token_secret",
        }

    def get_daily_summary(
        self, access_token: str, access_secret: str, target_date: date
    ) -> GarminData:
        """
        Fetch sleep, wellness, activity for a day.
        If authenticated via garth, fetches real data. Otherwise mocks it.
        """
        if self.is_authenticated:
            return self._get_real_daily_summary(target_date)

        return self._get_mocked_daily_summary(target_date)

    def _get_real_daily_summary(self, target_date: date) -> GarminData:
        logger.info(f"Fetching REAL daily summary for {target_date}")
        try:
            date_str = target_date.isoformat()

            # Fetch User Summary (Steps, HR, Calories)
            user_summary = self.client.connectapi(
                f"/usersummary-service/usersummary/daily/{self.display_name}?calendarDate={date_str}"
            )

            # Fetch Sleep Data
            sleep_data = self.client.connectapi(
                f"/wellness-service/wellness/dailySleepData/{self.display_name}?date={date_str}"
            )

            summary = user_summary or {}
            sleep_dto = sleep_data.get("dailySleepDTO", {})

            return GarminData(
                date=target_date,
                # Sleep
                sleep_score=sleep_dto.get("sleepScores", {})
                .get("overall", {})
                .get("value"),
                total_sleep_minutes=int((sleep_dto.get("sleepTimeSeconds") or 0) / 60),
                deep_sleep_minutes=int((sleep_dto.get("deepSleepSeconds") or 0) / 60),
                light_sleep_minutes=int((sleep_dto.get("lightSleepSeconds") or 0) / 60),
                rem_sleep_minutes=int((sleep_dto.get("remSleepSeconds") or 0) / 60),
                awake_minutes=int((sleep_dto.get("awakeSleepSeconds") or 0) / 60),
                # Wellness
                resting_heart_rate=summary.get("restingHeartRate"),
                stress_score=summary.get("averageStressLevel"),
                body_battery=None,  # Often found in a different endpoint, skipped for now to avoid complexity
                # Activity
                steps=summary.get("totalSteps"),
                active_minutes=int((summary.get("activeSeconds") or 0) / 60),
                calories_burned=summary.get("totalKilocalories"),
                # Body Comp (Basic)
                # These might be in a different summary, keeping mocked values or defaults if missing
                raw_data={"user_summary": summary, "sleep_data": sleep_data},
            )

        except Exception as e:
            logger.error(f"Error fetching real data for {target_date}: {e}")
            raise

    def _get_mocked_daily_summary(self, target_date: date) -> GarminData:
        logger.info(f"Fetching MOCKED daily summary for {target_date}")

        # DEMO SCENARIO: Force "Red Zone" recovery for TODAY
        if target_date == date.today():
            return GarminData(
                date=target_date,
                sleep_score=55,  # Poor
                total_sleep_minutes=360,
                deep_sleep_minutes=40,
                light_sleep_minutes=200,
                rem_sleep_minutes=120,
                awake_minutes=30,
                body_battery=20,  # Low (ignored by agent, but consistent)
                stress_score=75,  # High (Critical trigger)
                resting_heart_rate=65,  # Elevated (Critical trigger)
                hrv=30,  # Low
                steps=4500,
                active_minutes=10,
                calories_burned=1800,
                weight_kg=75.5,
                body_fat_percentage=15.0,
                muscle_mass_kg=60.0,
                raw_data={"mock": "demo_scenario_red_zone", "date": str(target_date)},
            )

        day_seed = target_date.day
        return GarminData(
            date=target_date,
            sleep_score=70 + (day_seed % 30),
            total_sleep_minutes=420 + (day_seed * 10),
            deep_sleep_minutes=60 + (day_seed * 2),
            light_sleep_minutes=300,
            rem_sleep_minutes=60 + (day_seed * 2),
            awake_minutes=10,
            body_battery=60 + (day_seed % 40),
            stress_score=20 + (day_seed % 30),
            resting_heart_rate=55 + (day_seed % 5),
            hrv=40 + (day_seed % 20),
            steps=8000 + (day_seed * 100),
            active_minutes=45 + (day_seed * 2),
            calories_burned=2200 + (day_seed * 10),
            weight_kg=75.5,
            body_fat_percentage=15.0,
            muscle_mass_kg=60.0,
            raw_data={"mock": "data", "date": str(target_date)},
        )

    def get_activities(
        self, access_token: str, access_secret: str, start_date: date, end_date: date
    ) -> List[GarminActivity]:
        """
        Fetch workouts in date range.
        """
        if self.is_authenticated:
            return self._get_real_activities(start_date, end_date)

        return self._get_mocked_activities(start_date, end_date)

    def _get_real_activities(
        self, start_date: date, end_date: date
    ) -> List[GarminActivity]:
        logger.info(f"Fetching REAL activities from {start_date} to {end_date}")
        activities = []
        try:
            # Fetch activities list
            # Note: limit is hardcoded for safety
            fetched_activities = self.client.connectapi(
                f"/activitylist-service/activities/search/activities?startDate={start_date}&endDate={end_date}&limit=50"
            )

            for act in fetched_activities:
                act_type = act.get("activityType", {}).get("typeKey", "unknown")
                start_time_str = act.get("startTimeLocal")
                start_time = (
                    datetime.fromisoformat(start_time_str)
                    if start_time_str
                    else datetime.now()
                )

                # Create GarminActivity object
                # Safely handling types that might be None
                duration_min = float(act.get("duration", 0) or 0) / 60.0
                distance_km = float(act.get("distance", 0) or 0) / 1000.0

                activities.append(
                    GarminActivity(
                        activity_type=act_type,
                        start_time=start_time,
                        duration_minutes=duration_min,
                        distance_km=distance_km,
                        avg_hr=act.get("averageHR"),
                        max_hr=act.get("maxHR"),
                        elevation_gain=act.get("elevationGain"),
                        avg_pace=float(
                            act.get("averageSpeed", 0) or 0
                        ),  # Note: Garmin provides speed in m/s, might need conversion for pace
                        raw_data=act,
                    )
                )

            return activities

        except Exception as e:
            logger.error(f"Error fetching real activities: {e}")
            raise

    def _get_mocked_activities(
        self, start_date: date, end_date: date
    ) -> List[GarminActivity]:
        logger.info(f"Fetching MOCKED activities from {start_date} to {end_date}")
        activities = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.day % 2 == 0:
                activities.append(
                    GarminActivity(
                        activity_type="running",
                        start_time=datetime.combine(current_date, datetime.min.time())
                        + timedelta(hours=7),
                        duration_minutes=45.0,
                        distance_km=5.0,
                        avg_pace=9.0,
                        avg_hr=145,
                        max_hr=170,
                        elevation_gain=50.0,
                        vo2_max=52.0,
                        aerobic_training_effect=3.0,
                        anaerobic_training_effect=1.0,
                        raw_data={"mock": "activity", "id": f"run_{current_date}"},
                    )
                )
            elif current_date.day % 2 != 0:
                activities.append(
                    GarminActivity(
                        activity_type="strength",
                        start_time=datetime.combine(current_date, datetime.min.time())
                        + timedelta(hours=18),
                        duration_minutes=60.0,
                        exercise_count=8,
                        set_count=24,
                        avg_hr=120,
                        max_hr=150,
                        raw_data={"mock": "activity", "id": f"strength_{current_date}"},
                    )
                )
            current_date += timedelta(days=1)
        return activities

    def get_body_composition(
        self, access_token: str, access_secret: str, start_date: date, end_date: date
    ) -> List[Dict[str, Any]]:
        # For brevity, leaving as mocked unless needed
        return [{"date": start_date, "weight": 75.5, "body_fat": 15.0}]

    def sync_user_data(
        self,
        user_id: str,
        access_token: str = "mock_token",
        access_secret: str = "mock_secret",
        days_back: int = 30,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Complete sync operation.
        """
        if email and password:
            try:
                self.login(email, password)
            except Exception as e:
                logger.error(f"Login failed during sync: {e}")
                return {
                    "user_id": user_id,
                    "status": "error",
                    "error": f"Login failed: {str(e)}",
                }

        logger.info(f"Syncing data for user {user_id} for last {days_back} days")

        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)

        # Pass dummy tokens if authenticated via garth
        # The methods inside will use self.client if authenticated
        activities = self.get_activities(
            access_token, access_secret, start_date, end_date
        )
        daily_summaries = []

        current = start_date
        while current <= end_date:
            try:
                summary = self.get_daily_summary(access_token, access_secret, current)
                daily_summaries.append(summary)
            except Exception as e:
                logger.warning(f"Failed to fetch summary for {current}: {e}")
            current += timedelta(days=1)

        return {
            "user_id": user_id,
            "period": f"{start_date} to {end_date}",
            "synced_days": len(daily_summaries),
            "activities_count": len(activities),
            "status": "success",
            "sample_data": {
                "latest_summary": daily_summaries[-1].model_dump()
                if daily_summaries
                else None,
                "latest_activity": activities[-1].model_dump() if activities else None,
            },
        }

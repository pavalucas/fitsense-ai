import logging
import os
from datetime import date

import garth
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("GarminDebug")


def main():
    # Load .env from current directory or backend directory
    load_dotenv()
    if not os.getenv("GARMIN_EMAIL"):
        load_dotenv("backend/.env")

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")

    if not email or not password:
        logger.error("Please set GARMIN_EMAIL and GARMIN_PASSWORD in .env file")
        return

    logger.info(f"Attempting to authenticate as {email}...")

    try:
        # 1. Authenticate
        garth.login(email, password)
        logger.info("Authentication successful.")

        # 2. Inspect Client State
        logger.info(f"Garth Username: {garth.client.username}")
        logger.info(f"Client Attributes: {dir(garth.client)}")

        # 3. Resolve Display Name
        # Try to fetch social profile to get the exact displayName used in URLs
        display_name = garth.client.username
        try:
            profile = garth.client.connectapi("/userprofile-service/socialProfile")
            if profile:
                logger.info(
                    f"Social Profile found. DisplayName: {profile.get('displayName')}"
                )
                display_name = profile.get("displayName")
            else:
                logger.warning("Social Profile returned None")
        except Exception as e:
            logger.error(f"Error fetching social profile: {e}")

        # Override from env if set
        env_display_name = os.getenv("GARMIN_DISPLAY_NAME")
        if env_display_name:
            logger.info(f"Overriding display name from .env: {env_display_name}")
            display_name = env_display_name

        logger.info(f"Using Display Name for requests: {display_name}")

        # 4. Test Data Fetching
        target_date = date.today().isoformat()
        logger.info(f"Attempting to fetch data for {target_date}...")

        # URL 1: User Summary
        summary_url = f"/usersummary-service/usersummary/daily/{display_name}?calendarDate={target_date}"
        logger.info(f"Requesting: {summary_url}")
        try:
            summary = garth.client.connectapi(summary_url)
            logger.info("✅ User Summary fetch successful!")
            logger.info(f"Keys: {list(summary.keys())}")
        except Exception as e:
            logger.error(f"❌ User Summary fetch failed: {e}")

        # URL 2: Sleep Data
        sleep_url = f"/wellness-service/wellness/dailySleepData/{display_name}?date={target_date}"
        logger.info(f"Requesting: {sleep_url}")
        try:
            sleep = garth.client.connectapi(sleep_url)
            logger.info("✅ Sleep Data fetch successful!")
        except Exception as e:
            logger.error(f"❌ Sleep Data fetch failed: {e}")

    except Exception as e:
        logger.error(f"Fatal error during execution: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

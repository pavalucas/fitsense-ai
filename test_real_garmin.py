import os
import sys
from datetime import date, timedelta

from dotenv import load_dotenv

# Add backend directory to path so we can import app modules
# Assuming this script is located at fitsense-ai/test_real_garmin.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

try:
    from app.services.garmin_service import GarminService
except ImportError as e:
    print(f"Error importing GarminService: {e}")
    sys.exit(1)


def test_real_garmin():
    print("=== Testing REAL Garmin Integration ===\n")

    # Load credentials from .env file
    # Look for .env in the current directory (fitsense-ai/)
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(env_path)

    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    display_name = os.getenv("GARMIN_DISPLAY_NAME")

    if not email or not password:
        print("❌ Error: GARMIN_EMAIL and GARMIN_PASSWORD not found.")
        print(f"Please create a .env file at: {env_path}")
        print("Format:")
        print("GARMIN_EMAIL=your_email@example.com")
        print("GARMIN_PASSWORD=your_password")
        print("GARMIN_DISPLAY_NAME=your_display_name (optional)")
        return

    print(f"Attempting to login as: {email}")

    try:
        # Initialize Service with credentials - this triggers the login
        service = GarminService(
            email=email, password=password, display_name=display_name
        )
        print("✅ Login successful!")
    except Exception as e:
        print(f"❌ Login failed: {e}")
        print("Please check your credentials.")
        return

    # 1. Test Daily Summary (Real Data)
    today = date.today()
    print(f"\n--- Fetching Real Data for Today ({today}) ---")

    try:
        # We pass dummy tokens because the service is authenticated via garth session
        summary = service.get_daily_summary("dummy_token", "dummy_secret", today)

        print("Health Metrics:")
        print(f"  - Steps: {summary.steps}")
        print(f"  - Resting HR: {summary.resting_heart_rate} bpm")
        print(f"  - Stress Score: {summary.stress_score}")
        print(f"  - Sleep Score: {summary.sleep_score}")
        print(
            f"  - Sleep Duration: {summary.total_sleep_minutes // 60}h {summary.total_sleep_minutes % 60}m"
        )

        if summary.raw_data:
            print("  (Raw data fetched successfully)")
        else:
            print("  (No raw data available)")

    except Exception as e:
        print(f"⚠️ Failed to fetch summary: {e}")

    # 2. Test Activities (Real Data)
    days_back = 14
    start_date = today - timedelta(days=days_back)
    print(f"\n--- Fetching Activities (Last {days_back} Days) ---")

    try:
        activities = service.get_activities(
            "dummy_token", "dummy_secret", start_date, today
        )
        print(f"Found {len(activities)} activities.")

        for i, act in enumerate(activities):
            type_str = act.activity_type.upper() if act.activity_type else "UNKNOWN"
            dist_str = f"{act.distance_km:.2f}km" if act.distance_km else "N/A"
            dur_str = f"{act.duration_minutes:.1f}min"
            hr_str = f"{act.avg_hr}bpm" if act.avg_hr else "N/A"

            print(
                f" {i + 1}. [{act.start_time.strftime('%Y-%m-%d %H:%M')}] {type_str}: {dist_str} in {dur_str} (HR: {hr_str})"
            )

    except Exception as e:
        print(f"⚠️ Failed to fetch activities: {e}")

    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_real_garmin()

import json
import os
import sys
from datetime import date, timedelta

# Add backend directory to path so we can import app modules
# Assuming this script is located at fitsense-ai/test_garmin_integration.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "backend")))

try:
    from app.services.garmin_service import GarminService
except ImportError as e:
    print(f"Error importing GarminService: {e}")
    print(
        "Make sure you are running this script from the project root or fitsense-ai directory."
    )
    sys.exit(1)


def test_garmin_flow():
    print("=== Testing Garmin Integration Flow ===\n")

    # Initialize Service
    try:
        service = GarminService()
        print("1. Service Initialized Successfully")
    except Exception as e:
        print(f"Failed to initialize service: {e}")
        return

    # 1. OAuth Flow Simulation
    print("\n--- Step 1: OAuth Authentication Flow ---")
    # Get the authorization URL (normally redirected to user)
    oauth_data = service.get_oauth_url()
    print(f"OAuth URL generated: {oauth_data['url']}")
    print(f"OAuth Token: {oauth_data['oauth_token']}")

    # Simulate callback with verifier
    mock_verifier = "mock_verifier"
    print(f"Simulating callback with verifier: {mock_verifier}")

    try:
        tokens = service.exchange_token(oauth_data["oauth_token"], mock_verifier)
        print(f"Tokens exchanged successfully.")
        print(f"Access Token: {tokens['access_token']}")
        print(f"Access Secret: {tokens['access_token_secret']}")

        access_token = tokens["access_token"]
        access_secret = tokens["access_token_secret"]
    except Exception as e:
        print(f"Token exchange failed: {e}")
        return

    # 2. Fetch Daily Summary
    print("\n--- Step 2: Fetching Daily Health Summary ---")
    today = date.today()
    try:
        summary = service.get_daily_summary(access_token, access_secret, today)
        print(f"Daily Summary Data for {today}:")
        print(f"  - Sleep Score: {summary.sleep_score}/100")
        print(f"  - Body Battery: {summary.body_battery}/100")
        print(f"  - Steps: {summary.steps}")
        print(f"  - Resting HR: {summary.resting_heart_rate} bpm")
        print(f"  - Stress Score: {summary.stress_score}")
    except Exception as e:
        print(f"Failed to fetch daily summary: {e}")

    # 3. Fetch Activities
    print("\n--- Step 3: Fetching Recent Activities ---")
    days_to_fetch = 5
    start_date = today - timedelta(days=days_to_fetch)
    print(f"Fetching activities from {start_date} to {today}...")

    try:
        activities = service.get_activities(
            access_token, access_secret, start_date, today
        )
        print(f"Found {len(activities)} activities:")

        for activity in activities:
            print(f"  [{activity.start_time.date()}] {activity.activity_type.upper()}:")
            print(f"    Duration: {activity.duration_minutes} min")
            print(f"    Avg HR: {activity.avg_hr} bpm")

            if activity.activity_type == "running":
                print(f"    Distance: {activity.distance_km} km")
                print(f"    Pace: {activity.avg_pace} min/km")
            elif activity.activity_type == "strength":
                print(f"    Exercises: {activity.exercise_count}")
                print(f"    Sets: {activity.set_count}")
            print("")

    except Exception as e:
        print(f"Failed to fetch activities: {e}")

    # 4. Full Sync Simulation
    print("\n--- Step 4: Simulating Full User Data Sync ---")
    user_id = "user_demo_123"
    print(f"Triggering sync for user {user_id}...")

    try:
        sync_result = service.sync_user_data(
            user_id, access_token, access_secret, days_back=7
        )

        print("Sync completed successfully!")
        print("Summary of synced data:")
        # Print a simplified version of the result
        print(f"  Period: {sync_result['period']}")
        print(f"  Days Synced: {sync_result['synced_days']}")
        print(f"  Activities Synced: {sync_result['activities_count']}")
        print(f"  Status: {sync_result['status']}")

    except Exception as e:
        print(f"Sync failed: {e}")

    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_garmin_flow()

TEST_SCENARIOS = [
    {
        "name": "Overtrained Marathoner",
        "description": "An advanced runner with high recent load and poor recovery metrics. Expecting a deload/recovery week.",
        "agent_target": "planning_agent",
        "input_data": {
            "user_profile": {
                "fitness_level": "Advanced",
                "goals": ["Marathon Performance"],
                "equipment": ["Running Shoes", "GPS Watch"],
                "limitations": [],
            },
            "recent_workouts": [
                {
                    "date": "2023-10-01",
                    "type": "Long Run",
                    "distance_km": 32.0,
                    "duration_min": 180,
                    "avg_hr": 155,
                },
                {
                    "date": "2023-10-03",
                    "type": "Tempo Run",
                    "distance_km": 12.0,
                    "duration_min": 55,
                    "avg_hr": 165,
                },
                {
                    "date": "2023-10-04",
                    "type": "Easy Run",
                    "distance_km": 8.0,
                    "duration_min": 45,
                    "avg_hr": 135,
                },
            ],
            "recovery_status": {
                "recovery_status": "poor",
                "recovery_score": 35,
                "key_metrics_summary": {
                    "body_battery": "Low (30)",
                    "sleep_quality": "Poor (Score: 55)",
                    "stress_level": "High",
                    "rhr_trend": "Elevated",
                },
            },
        },
        "expected_outcome_criteria": [
            "Weekly volume should be significantly reduced compared to recent activity.",
            "Intensity should be mostly 'Low' or 'Recovery'.",
            "At least 2 complete rest days should be scheduled.",
        ],
    },
    {
        "name": "Beginner Weight Loss",
        "description": "A beginner with no equipment looking to lose weight. Expecting simple, consistent, low-barrier exercises.",
        "agent_target": "planning_agent",
        "input_data": {
            "user_profile": {
                "fitness_level": "Beginner",
                "goals": ["Weight Loss", "General Health"],
                "equipment": ["None (Bodyweight)"],
                "limitations": ["Low endurance"],
            },
            "recent_workouts": [],
            "recovery_status": {
                "recovery_status": "good",
                "recovery_score": 85,
                "key_metrics_summary": {
                    "body_battery": "High (90)",
                    "sleep_quality": "Good (Score: 85)",
                    "stress_level": "Low",
                    "rhr_trend": "Stable",
                },
            },
        },
        "expected_outcome_criteria": [
            "Exercises should be bodyweight only.",
            "Intensity should be 'Low' to 'Moderate'.",
            "Focus on consistency (3-4 workouts per week).",
            "Includes walking or simple cardio.",
        ],
    },
    {
        "name": "Intermediate Hypertrophy",
        "description": "Intermediate lifter with gym access wanting muscle gain. Good recovery. Expecting progressive overload.",
        "agent_target": "planning_agent",
        "input_data": {
            "user_profile": {
                "fitness_level": "Intermediate",
                "goals": ["Muscle Gain (Hypertrophy)"],
                "equipment": ["Full Gym"],
                "limitations": [],
            },
            "recent_workouts": [
                {
                    "date": "2023-10-01",
                    "type": "Upper Body Strength",
                    "duration_min": 60,
                    "intensity": "Moderate",
                },
                {
                    "date": "2023-10-03",
                    "type": "Lower Body Strength",
                    "duration_min": 60,
                    "intensity": "High",
                },
            ],
            "recovery_status": {
                "recovery_status": "excellent",
                "recovery_score": 92,
                "key_metrics_summary": {
                    "body_battery": "High (95)",
                    "sleep_quality": "Excellent (Score: 90)",
                    "stress_level": "Low",
                    "rhr_trend": "Stable",
                },
            },
        },
        "expected_outcome_criteria": [
            "Plan should include split routines (e.g., Push/Pull/Legs or Upper/Lower).",
            "Volume should be moderate to high (3-4 sets per exercise).",
            "Intensity should be 'Moderate' to 'High'.",
        ],
    },
    {
        "name": "Critical Recovery Adaptation",
        "description": "User has a hard workout scheduled but woke up with terrible recovery metrics. Expecting adaptation to rest.",
        "agent_target": "adaptation_agent",
        "input_data": {
            "scheduled_workout": {
                "type": "HIIT Intervals",
                "duration_min": 45,
                "intensity": "High",
                "exercises": ["Sprints", "Burpees", "Jump Squats"],
            },
            "today_recovery": {
                "body_battery": 25,
                "sleep_score": 45,
                "resting_heart_rate": 65,  # Baseline 55
                "stress_score": 75,
            },
            "recent_training_load": {
                "load_focus": "High Aerobic",
                "acute_load": 1200,  # High for this user
            },
        },
        "expected_outcome_criteria": [
            "Modification status should be 'modified' or 'cancelled_for_rest'.",
            "New intensity should be 'Low'.",
            "Safety check should flag low sleep and body battery.",
        ],
    },
]

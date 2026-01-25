import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Adjust import based on how the app is run (module vs script)
try:
    from app.services.garmin_service import GarminService
except ImportError:
    from services.garmin_service import GarminService

load_dotenv()

app = FastAPI(title="FitSense AI API")

# CORS configuration
# Allowing all for hackathon flexibility, refine for production
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Garmin Service
# We try to initialize with env vars. If not present, it will run in mock mode
# unless login is called later.
garmin_email = os.getenv("GARMIN_EMAIL")
garmin_password = os.getenv("GARMIN_PASSWORD")
garmin_display_name = os.getenv("GARMIN_DISPLAY_NAME")

garmin_service = GarminService(
    email=garmin_email, password=garmin_password, display_name=garmin_display_name
)


@app.get("/")
async def read_root():
    """
    Root endpoint to verify API is running.
    """
    return {
        "message": "Welcome to FitSense AI API",
        "docs_url": "/docs",
        "garmin_status": "Authenticated"
        if garmin_service.is_authenticated
        else "Mock Mode",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/api/garmin/sync/{user_id}")
async def sync_garmin_data(user_id: str, days: int = 7):
    """
    Trigger a sync of Garmin data for a specific user.
    If backend is authenticated with real Garmin creds, fetches real data.
    Otherwise returns mocked data.
    """
    try:
        # In a real scenario, user-specific tokens would be retrieved here.
        # Since we are using a single account for the hackathon demo or mock data:
        result = garmin_service.sync_user_data(
            user_id=user_id,
            access_token="mock_token",  # Handled internally by service if using garth
            access_secret="mock_secret",
            days_back=days,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

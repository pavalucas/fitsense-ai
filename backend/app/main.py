import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Adjust import based on how the app is run (module vs script)
try:
    from app.dependencies import get_garmin_service
    from app.routers.coach import router as coach_router
    from app.services.garmin_service import GarminService
except ImportError:
    from dependencies import get_garmin_service
    from routers.coach import router as coach_router
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

# Include Routers
app.include_router(coach_router)

# Initialize Garmin Service
# We try to initialize with env vars. If not present, it will run in mock mode
# unless login is called later.
garmin_service = get_garmin_service()


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


class GarminAuthRequest(BaseModel):
    email: str
    password: str


@app.post("/api/garmin/auth")
async def authenticate_garmin(request: GarminAuthRequest):
    """
    Verify Garmin credentials.
    """
    try:
        # Try to login to verify credentials
        garmin_service.login(request.email, request.password)
        return {"status": "success", "message": "Authentication successful"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


class GarminSyncRequest(BaseModel):
    email: str
    password: str
    days: int = 7


@app.post("/api/garmin/sync/{user_id}")
async def sync_garmin_data_post(user_id: str, request: GarminSyncRequest):
    """
    Trigger a sync of Garmin data for a specific user using provided credentials.
    """
    try:
        result = garmin_service.sync_user_data(
            user_id=user_id,
            email=request.email,
            password=request.password,
            days_back=request.days,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/garmin/sync/{user_id}")
async def sync_garmin_data_get(user_id: str, days: int = 7):
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

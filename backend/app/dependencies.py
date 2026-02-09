import os

from app.services.coach_orchestrator import CoachOrchestrator
from app.services.garmin_service import GarminService
from dotenv import load_dotenv

load_dotenv()

# Global instances for dependency injection
# In a production app, these might be scoped per request or handled via a more robust DI framework
_garmin_service = None
_coach_orchestrator = None


def get_garmin_service() -> GarminService:
    """
    Returns a singleton-like instance of GarminService.
    Initializes it if not already initialized.
    """
    global _garmin_service
    if _garmin_service is None:
        email = os.getenv("GARMIN_EMAIL")
        password = os.getenv("GARMIN_PASSWORD")
        display_name = os.getenv("GARMIN_DISPLAY_NAME")

        # Initialize with credentials if available, otherwise it defaults to mock mode
        _garmin_service = GarminService(
            email=email, password=password, display_name=display_name
        )

    return _garmin_service


def get_coach_orchestrator() -> CoachOrchestrator:
    """
    Returns a singleton-like instance of CoachOrchestrator.
    Initializes it if not already initialized.
    """
    global _coach_orchestrator
    if _coach_orchestrator is None:
        garmin_service = get_garmin_service()
        _coach_orchestrator = CoachOrchestrator(garmin_service=garmin_service)

    return _coach_orchestrator

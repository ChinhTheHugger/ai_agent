from .geocoding import get_geocoding
from .weather import current_weather_api
from .simple_user_io import ask_user, response_user

# The complete registry of all system actions
TOOL_REGISTRY = {
    "get_geocoding": get_geocoding,
    "get_current_weather": current_weather_api,
    "ask_user": ask_user,
    "response_user": response_user  # Registered alongside the others!
}
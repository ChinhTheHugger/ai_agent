import requests

API_KEY = 'e1614efbfe8be4797e83cfadf361631f'

def current_weather_api(location: dict, time: str = "current") -> str:
    """
    Action Tool: Fetches raw weather data from OpenWeather map.
    Expects location dict containing {'lat': float, 'lon': float}
    """
    try:
        lat = location.get('lat')
        lon = location.get('lon')
        
        url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric'
        res = requests.get(url)
        
        # We send the RAW text response straight back to the Agent without any cleaning!
        return res.text
    except Exception as e:
        return f'{{"error": "Failed to fetch from OpenWeather API: {str(e)}"}}'
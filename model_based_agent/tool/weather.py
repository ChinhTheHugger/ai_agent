import requests
from pathlib import Path
import json

def current_weather_api(location: dict) -> str:
    """
    Action Tool: Fetches raw weather data from external weather service.
    Expects location dict containing {'lat': float, 'lon': float}
    """
    
    current_dir = Path(__file__).resolve()
    api_key_dir = current_dir.parent.parent.parent.parent / "file" / "weather_api_key.json"

    with open(api_key_dir, 'r') as file:
        data = json.load(file)
    
    try:
        lat = location.get('lat')
        lon = location.get('lon')
        
        # # OpenWeather
        # url = f'''https://api.openweathermap.org/data/4.0/onecall/current?lat=52.2297&lon=21.0122&units=metric&lang=en&appid={data['OpenWeather']}'''

        # WeatherAPI
        url = f'''http://api.weatherapi.com/v1/current.json?key={data['WeatherAPI']}&q={lat},{lon}'''
        
        res = requests.get(url)
        
        # We send the RAW text response straight back to the Agent without any cleaning!
        return res.text
    except Exception as e:
        return f'{{"error": "Failed to fetch from external API: {str(e)}"}}'
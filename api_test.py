import requests
from pathlib import Path
import json

current_dir = Path(__file__).resolve()
api_key_dir = current_dir.parent.parent / "file" / "weather_api_key.json"

with open(api_key_dir, 'r') as file:
    data = json.load(file)


# --- OpenWeather ---

# res = requests.get(f'''https://api.openweathermap.org/data/2.5/onecall/weather?lat=52.2297&lon=21.0122&units=metric&lang=en&appid={data['OpenWeather']}''')


# --- WeatherAPI ---

# res = requests.get(f'''http://api.weatherapi.com/v1/current.json?key={data['WeatherAPI']}&q=35.68388282018455,139.6927064529045''')


# --- Open-Meteo ---

# res = requests.get('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m')


# Geocoding

res = requests.get(f'''https://geocode.maps.co/search?q=Tokyo&api_key={data['GeocodingAPI']}''')


print(res.text)
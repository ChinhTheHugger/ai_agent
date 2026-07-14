import requests
from pathlib import Path
import json

def get_geocoding(location: str) -> str:
    """
    Action Tool: Fetches geocoding data from external map service.
    Expects address as text
    """
    
    current_dir = Path(__file__).resolve()
    api_key_dir = current_dir.parent.parent.parent.parent / "file" / "weather_api_key.json"
    
    with open(api_key_dir, 'r') as file:
        data = json.load(file)
    
    try:
        url = f'''https://geocode.maps.co/search?q={location}&api_key={data['GeocodingAPI']}'''
        
        res = requests.get(url)
        
        # We send the RAW text response straight back to the Agent without any cleaning!
        return res.text
    except Exception as e:
        return f'{{"error": "Failed to fetch from external API: {str(e)}"}}'
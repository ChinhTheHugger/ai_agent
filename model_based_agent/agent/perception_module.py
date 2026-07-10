import json
import datetime

def get_perception_instructions() -> str:
    """Generates the system prompt containing default states and strict extraction guardrails."""
    current_time_str = datetime.datetime.now().strftime("%I:%M %p")
    default_location = "Hanoi"
    
    return (
        f"You are a weather perception module. Analyze the user's input.\n"
        f"1. Extract the 'location' and 'time'.\n"
        f"2. If no location is mentioned, use the default: '{default_location}'.\n"
        f"3. If no time is mentioned, use the current time: '{current_time_str}'.\n"
        f"4. CRITICAL: If the user is NOT asking about weather or temperature, you must return: "
        f"{{\"error\": \"Not a weather query\"}}.\n"
        f"Output ONLY valid JSON matching this schema: \n"
        f"{{\"location\": \"string\", \"time\": \"string\"}} or {{\"error\": \"reason\"}}"
    )

def parse_raw_api_weather(raw_json_text: str) -> str:
    """
    New Perception Job: Takes the massive, raw OpenWeather text response 
    and filters out only what the brain needs for natural language synthesis.
    """
    try:
        data = json.loads(raw_json_text)
        
        # Handle API error structures safely
        if "error" in data or "cod" in data and data["cod"] != 200:
            return f"Error from weather service: {data.get('message', 'Unknown failure')}"
            
        # Parse out specific variables from the raw OpenWeather OneCall JSON payload
        current_data = data.get("current", {})
        temp = current_data.get("temp")
        humidity = current_data.get("humidity")
        weather_desc = current_data.get("weather", [{}])[0].get("description", "unknown conditions")
        
        # Build a clean micro-summary for our Brain's synthesis layer
        summary = f"Temperature is {temp}°C, humidity is {humidity}%, condition is {weather_desc}."
        return summary
        
    except Exception as e:
        return f"Perception processing failed to extract API data: {str(e)}"
import json

def parse_perception_output(raw_text: str) -> dict:
    """Safely decodes raw string text into structured Python dictionaries."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        return {"error": "Format violation: Perception string was not valid JSON."}

def parse_user_input(user_input) -> str:
    """Convert data sent by user input device into text for LLM."""
    """Suitable conversion is selected based on device classification"""
    
    return user_input

def parse_user_output(user_output) -> str:
    """Convert data sent by LLM into compatible format for user output device."""
    
    return user_output
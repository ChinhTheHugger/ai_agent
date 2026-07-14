import datetime

def user_input_perception_instructions() -> str:
    """Generates the system prompt containing default states and strict extraction guardrails for processing user input."""
    current_time_str = datetime.datetime.now().strftime("%I:%M %p")
    default_location = "Hanoi"
    
    return (
        f"You are a weather perception module. Analyze the user's input.\n"
        f"Extract the 'location' and 'time'\n"
        f"If no location is mentioned, use the default: '{default_location}'.\n"
        f"If no time is mentioned, use the current time: '{current_time_str}'.\n"
        f"If location contain multiple administrative levels, sort from smallest to largest.\n"
        f"After sorting, connect all administrative levels in location into one string, and replace spaces in between each words with plus sign '+'.\n"
        f"CRITICAL: If the user is NOT asking about weather or temperature, you must return: "
        f"{{\"error\": \"Your request was not a valid weather query\"}}.\n"
        f"Output ONLY valid JSON matching this schema: \n"
        f"{{\n"
        f"  \"location\": \"string\",\n"
        f"  \"time\": \"string\"\n"
        f"}}\n"
        f"or\n"
        f"{{\n"
        f"  \"error\": \"reason\"\n"
        f"}}\n"
    )

def user_output_perception_instructions() -> str:
    """Generates the system prompt containing strict extraction guardrails for processing output to be sent to user."""
    
    return (
        f"Convert the extract data into a friendly, natural language answer matching the language of the user's query.\n"
        f"CRITICAL: If an error is encountered during summarization, you must return:\n"
        f"\"I have encountered some errors and can't response to your request properly\"\n"
        f"Output ONLY valid text, either the weather summary or the predefined error response above."
    )

def geocoding_api_output_perception_instruction() -> str:
    """Generates the system prompt containing strict extraction guardrails for processing geocoding API's response."""
    
    return (
        f"Parse the geocoding API's response and extract data.\n"
        f"Extract the latitude and longitude of the location.\n"
        f"CRITICAL: If there is no detected data for latitude and longitude, you must return:\n"
        f"{{\"error\": \"Unable to find any valid geocoding information for your request\"}}.\n"
        f"CRITICAL: If the geocoding API's response contain error, you must return:\n"
        f"{{\"error\": \"The geocoding service has encountered some errors\"}}.\n"
        f"Output ONLY valid JSON matching this schema: \n"
        f"{{\n"
        f"  \"lat\": \"string\",\n"
        f"  \"lon\": \"string\"\n"
        f"}}\n"
        f"or\n"
        f"{{\n"
        f"  \"error\": \"reason\"\n"
        f"}}\n"
    )

def weather_api_output_perception_instruction() -> str:
    """Generates the system prompt containing strict extraction guardrails for processing weather API's response."""
    
    return (
        f"Parse the weather API's response and extract data.\n"
        f"Focus on these parameters: weather condition, temperature, humidity, wind speed, chances of various conditions like raining, snowing,...\n"
        f"If there is no detected data for a parameter, skip said parameter.\n"
        f"CRITICAL: If there is no detected data for all parameters, you must return:\n"
        f"{{\"error\": \"Unable to find any valid weather information for your request\"}}.\n"
        f"CRITICAL: If the weather API's response contain error, you must return:\n"
        f"{{\"error\": \"The weather service has encountered some errors\"}}.\n"
        f"Output ONLY valid JSON matching this schema: \n"
        f"{{\"parameter\": \"string\",...}} for each parameters, or {{\"error\": \"reason\"}}"
        f"Output ONLY valid JSON matching this schema: \n"
        f"{{\n"
        f"  \"parameter\": \"string\",\n"
        f"  ...\n"
        f"}}\n"
        f"for each parameters,\n"
        f"or\n"
        f"{{\n"
        f"  \"error\": \"reason\"\n"
        f"}}\n"
    )
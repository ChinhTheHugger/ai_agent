import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Notice we import parse_raw_api_weather now!
from agent.perception_module import parse_perception_output, parse_user_input, parse_user_output
from agent.action_module import execute_action
from agent.reasoning_module import user_input_perception_instructions, user_output_perception_instructions, geocoding_api_output_perception_instruction, weather_api_output_perception_instruction
from brain.brain import request_extraction, request_natural_language

def run_agent_orchestrator():
    print("================================================================")
    print("=== Multi-Module Weather Agent Active (Type 'exit' to quit) ===")
    print("================================================================")
    
    # Step 1: Wait for input
    raw_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - What would you like to know?"})
    user_input = parse_user_input(raw_input)
    
    while True:
        if user_input.lower() == 'exit':
            user_output = parse_user_output(f"{datetime.datetime.now()} - Shutting down modules. Goodbye!")
            execute_action("response_user", {"message": user_output})
            break
        if not user_input:
            raw_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - Anything else you would like to know?"})
            user_input = parse_user_input(raw_input)
            continue
        
        user_output = parse_user_output(f"{datetime.datetime.now()} - [Agent]: Triggering Perception Module (Input Extraction)...")
        execute_action("response_user", {"message": user_output})
        
        # Step 2: Cognition / Send input to DeepSeek (Extraction Phase)
        user_input_perception_rules = user_input_perception_instructions()
        raw_brain_extraction = request_extraction(user_input_perception_rules, user_input)
        extracted_context = parse_perception_output(raw_brain_extraction)
        
        # Guardrail error handling check
        if "error" in extracted_context.keys():
            user_output = parse_user_output(f"{datetime.datetime.now()} - [Agent Guardrail Alert]: {extracted_context['error']}")
            execute_action("response_user", {"message": user_output})
            
            user_output = parse_user_output(f"{datetime.datetime.now()} - I am sorry, I can only assist you with weather questions.")
            execute_action("response_user", {"message": user_output})
            
            raw_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - Anything else you would like to know?"})
            user_input = parse_user_input(raw_input)
            continue
            
        # Convert location into coordinates, e.g., {'lat': 21.0285, 'lon': 105.8542}
        location_text = extracted_context.get("location")
        action_args = {"location": location_text}
        raw_web_response = execute_action("get_geocoding", action_args)
        
        geocoding_perception_rules = geocoding_api_output_perception_instruction()
        raw_brain_extraction = request_extraction(geocoding_perception_rules, raw_web_response)
        extracted_context = parse_perception_output(raw_brain_extraction)
        
        # Guardrail error handling check
        if "error" in extracted_context.keys():
            user_output = parse_user_output(f"{datetime.datetime.now()} - [Agent Guardrail Alert]: {extracted_context['error']}")
            execute_action("response_user", {"message": user_output})
            
            user_output = parse_user_output(f"{datetime.datetime.now()} - The geocoding service failed: {extracted_context['error']}. Please try another city.")
            execute_action("response_user", {"message": user_output})
            
            raw_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - Anything else you would like to know?"})
            user_input = parse_user_input(raw_input)
            continue
        
        # Step 4: Triggering Action Module (Raw Web Request)
        location_coords = extracted_context
        user_output = parse_user_output(f"{datetime.datetime.now()} - [Agent]: Triggering Action Module (Fetching Live Weather Service JSON)...")
        execute_action("response_user", {"message": user_output})
        action_args = {"location": location_coords}
        raw_web_response = execute_action("get_current_weather", action_args)
        
        # --- THE CRITICAL MODIFICATION START ---
        
        user_output = parse_user_output(f"{datetime.datetime.now()} - [Agent]: Routing raw response to Perception Module for decoding...")
        execute_action("response_user", {"message": user_output})
        
        # We intercept the raw string and pass it to perception to extract the essentials
        weather_api_response_perception_rules = weather_api_output_perception_instruction()
        raw_brain_extraction = request_extraction(weather_api_response_perception_rules, raw_web_response)
        interpreted_observation = parse_perception_output(raw_brain_extraction)
        
        # --- THE CRITICAL MODIFICATION END ---
        
        # If the perception module flags an API error, handle it gracefully
        if "error" in interpreted_observation.keys():
            clarification_question = f"{datetime.datetime.now()} - The weather service failed: {interpreted_observation['error']}. Please try another city."
            raw_input = execute_action("ask_user", {"question": clarification_question})
            user_input = parse_user_input(raw_input)
            continue
        
        # Step 5: Send the clean, filtered observation to Brain for natural language conversion
        user_output = parse_user_output(f"{datetime.datetime.now()} - [Agent]: Sending interpreted data to Brain for synthesis...")
        execute_action("response_user", {"message": user_output})
        user_output_perception_rules = user_output_perception_instructions()
        final_human_answer = request_natural_language(user_output_perception_rules, user_input, raw_brain_extraction)
        
        # Step 6: Return final info to end user via user_io tool
        user_output = parse_user_output(f"{datetime.datetime.now()} - [Agent]: Triggering Action Module to present final answer...")
        execute_action("response_user", {"message": user_output})
        
        user_output = parse_user_output(f'{datetime.datetime.now()} - {final_human_answer}')
        execute_action("response_user", {"message": user_output})
        
        # Step 7: Get next input from user to keep the conversation going
        raw_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - Anything else you would like to know?"})
        user_input = parse_user_input(raw_input)

if __name__ == "__main__":
    run_agent_orchestrator()
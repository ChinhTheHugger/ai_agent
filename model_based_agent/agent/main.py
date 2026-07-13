import sys
import os
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Notice we import parse_raw_api_weather now!
from agent.perception_module import get_perception_instructions, parse_perception_output, parse_raw_api_weather
from agent.action_module import execute_action
from brain.brain import request_extraction, request_natural_language

def run_agent_orchestrator():
    print("================================================================")
    print("=== Multi-Module Weather Agent Active (Type 'exit' to quit) ===")
    print("================================================================")
    
    # Step 1: Wait for input
    user_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - What would you like to know?"})
    
    while True:
        if user_input.lower() == 'exit':
            execute_action("response_user", {"message": f"{datetime.datetime.now()} - Shutting down modules. Goodbye!"})
            break
        if not user_input:
            user_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - Anything else you would like to know?"})
            continue
        
        execute_action("response_user", {"message": f"{datetime.datetime.now()} - [Agent]: Triggering Perception Module (Input Extraction)..."})
        perception_rules = get_perception_instructions()
        
        # Step 2: Cognition / Send input to DeepSeek (Extraction Phase)
        raw_brain_extraction = request_extraction(perception_rules, user_input)
        extracted_context = parse_perception_output(raw_brain_extraction)
        
        # Guardrail error handling check
        if "error" in extracted_context:
            execute_action("response_user", {"message": f"{datetime.datetime.now()} - [Agent Guardrail Alert]: {extracted_context['error']}"})
            execute_action("response_user", {"message": f"{datetime.datetime.now()} - I am sorry, I can only assist you with weather questions."})
            user_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - Anything else you would like to know?"}) 
            continue
            
        # These are now coordinates! E.g., {'lat': 21.0285, 'lon': 105.8542}
        location_coords = extracted_context.get("location") 
        time = extracted_context.get("time")
        
        # Step 4: Triggering Action Module (Raw Web Request)
        execute_action("response_user", {"message": f"{datetime.datetime.now()} - [Agent]: Triggering Action Module (Fetching Live Weather Service JSON)..."})
        action_args = {"location": location_coords, "time": time}
        raw_web_response = execute_action("get_current_weather", action_args)
        
        # --- THE CRITICAL MODIFICATION START ---
        execute_action("response_user", {"message": f"{datetime.datetime.now()} - [Agent]: Routing raw response to Perception Module for decoding..."})
        # We intercept the raw string and pass it to perception to extract the essentials
        interpreted_observation = parse_raw_api_weather(raw_web_response)
        execute_action("response_user", {"message": f"{datetime.datetime.now()} - I am sorry, I can only assist you with weather questions."})
        execute_action("response_user", {"message": f"{datetime.datetime.now()} - [Agent Filtered Observation]: {interpreted_observation}"})
        # --- THE CRITICAL MODIFICATION END ---
        
        # If the perception module flags an API error, handle it gracefully
        if "Error" in interpreted_observation:
            clarification_question = f"{datetime.datetime.now()} - The weather service failed: {interpreted_observation}. Please try another city."
            user_input = execute_action("ask_user", {"question": clarification_question})
            continue 
        
        # Step 5: Send the clean, filtered observation to Brain for natural language conversion
        execute_action("response_user", {"message": f"{datetime.datetime.now()} - [Agent]: Sending interpreted data to Brain for synthesis..."})
        final_human_answer = request_natural_language(user_input, interpreted_observation)
        
        # Step 6: Return final info to end user via user_io tool
        execute_action("response_user", {"message": f"{datetime.datetime.now()} - [Agent]: Triggering Action Module to present final answer..."})
        execute_action("response_user", {"message": f'{datetime.datetime.now()} - {final_human_answer}'})
        
        # Step 7: Get next input from user to keep the conversation going
        user_input = execute_action("ask_user", {"question": f"{datetime.datetime.now()} - Anything else you would like to know?"})

if __name__ == "__main__":
    run_agent_orchestrator()
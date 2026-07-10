import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.perception_module import get_perception_instructions, parse_raw_api_weather
from agent.action_module import execute_action
from brain.brain import request_extraction, request_natural_language

def run_agent_orchestrator():
    print("================================================================")
    print("=== Multi-Module Weather Agent Active (Type 'exit' to quit) ===")
    print("================================================================")
    
    # Step 1: Initial wait for user input
    user_input = input("\nYou: ").strip()
    
    while True:
        if user_input.lower() == 'exit':
            print("Shutting down modules. Goodbye!")
            break
        if not user_input:
            user_input = input("\nYou: ").strip()
            continue
            
        print("[Agent]: Triggering Perception Module...")
        perception_rules = get_perception_instructions()
        
        # Step 2: Cognition Phase (Extraction)
        raw_brain_extraction = request_extraction(perception_rules, user_input)
        extracted_context = parse_raw_api_weather(raw_brain_extraction)
        
        # Guardrail error handling check
        if "error" in extracted_context:
            print(f"[Agent Guardrail Alert]: {extracted_context['error']}")
            # Use response_user tool to declare the restriction instead of hardcoded print
            execute_action("response_user", {"message": "I am sorry, I can only assist you with weather questions."})
            user_input = input("\nYou: ").strip() 
            continue
            
        location = extracted_context.get("location")
        time = extracted_context.get("time")
        
        # Step 4: Triggering Action Module for Weather data collection
        print("[Agent]: Triggering Action Module for Weather...")
        action_args = {"location": location, "time": time}
        raw_observation = execute_action("get_current_weather", action_args)
        print(f"[Agent Observation Captured]: {raw_observation}")
        
        # If the weather tool failed, trigger Human-in-the-Loop clarification
        if "ERROR" in raw_observation:
            clarification_question = f"I couldn't find weather data for '{location}'. Did you mean a different city?"
            user_input = execute_action("ask_user", {"question": clarification_question})
            continue 
        
        # Step 5: Send raw tool observation back to Brain for natural language conversion
        print("[Agent]: Sending observation to Brain for synthesis...")
        final_human_answer = request_natural_language(user_input, raw_observation)
        
        # Step 6: *UPDATED* Return final info using the Action Module!
        print("[Agent]: Triggering Action Module to present final answer...")
        delivery_status = execute_action("response_user", {"message": final_human_answer})
        print(f"[Agent Action Status]: {delivery_status}")
        
        # Step 7: Get next input from user to keep the conversation going
        user_input = input("\nYou: ").strip()

if __name__ == "__main__":
    run_agent_orchestrator()
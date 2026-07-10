import json

def turn_on_light(room: str) -> str:
    return f"Success: The light in the {room} has been turned ON."

def set_thermostat(temperature: int) -> str:
    return f"Success: Thermostat target set to {temperature}°C."

def rule_based_brain(user_input: str) -> str:
    """
    Acts like the LLM but uses rigid string rules.
    Crucially, it MUST output a strict JSON format that our Agent can parse.
    """
    clean_input = user_input.lower()
    
    # Rule 1: Look for light commands
    if "turn on the light in the" in clean_input:
        # Extract the room name from the sentence
        room = clean_input.split("in the ")[-1].strip()
        response = {
            "status": "CALL_TOOL",
            "tool_name": "turn_on_light",
            "arguments": {"room": room}
        }
    
    # Rule 2: Look for temperature commands
    elif "set temperature to" in clean_input:
        # Extract the number from the sentence
        words = clean_input.split()
        try:
            temp = int([w for w in words if w.isdigit()][0])
            response = {
                "status": "CALL_TOOL",
                "tool_name": "set_thermostat",
                "arguments": {"temperature": temp}
            }
        except IndexError:
            response = {"status": "FINAL_ANSWER", "message": "I heard a temperature command, but couldn't find the numbers."}
            
    # Rule 3: Fallback if no rules match
    else:
        response = {
            "status": "FINAL_ANSWER",
            "message": "I'm sorry, I don't know how to handle that request yet."
        }
        
    return json.dumps(response)

def run_agent_loop(user_query: str):
    print(f"\n[User]: {user_query}")
    
    # Step 1: Send raw input to the brain
    brain_raw_output = rule_based_brain(user_query)
    
    # Step 2: The Agent parses the format
    try:
        brain_data = json.loads(brain_raw_output)
    except json.JSONDecodeError:
        print("[Agent Error]: Brain did not return valid JSON!")
        return

    # Step 3: Determine if a tool is needed or if we are finished
    if brain_data.get("status") == "FINAL_ANSWER":
        print(f"[Agent Final Answer]: {brain_data['message']}")
        return

    if brain_data.get("status") == "CALL_TOOL":
        tool_name = brain_data.get("tool_name")
        args = brain_data.get("arguments", {})
        
        print(f"[Agent Orchestration]: Brain requested tool '{tool_name}' with args {args}")
        
        # Step 4: Execute the tool based on the brain's decision
        if tool_name == "turn_on_light":
            tool_result = turn_on_light(room=args.get("room"))
        elif tool_name == "set_thermostat":
            tool_result = set_thermostat(temperature=args.get("temperature"))
        else:
            # Edge Case Handling: Brain hallucinated a tool name
            tool_result = f"Error: Tool '{tool_name}' is not registered in this system."
        
        # Step 5: Feed the tool result back into the system (simulating the final pass)
        print(f"[Tool Output Received]: {tool_result}")
        print(f"[Agent Final Answer]: Task completed successfully. {tool_result}")

if __name__ == "__main__":
    # Test Case 1: Valid Light Command
    run_agent_loop("Please turn on the light in the kitchen")
    
    # Test Case 2: Valid Temperature Command
    run_agent_loop("Set temperature to 22 degrees")
    
    # Test Case 3: Triggers the fallback rule
    run_agent_loop("Can you order a pizza?")
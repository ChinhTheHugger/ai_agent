from tool import TOOL_REGISTRY

def execute_action(tool_name: str, arguments: dict) -> str:
    """
    The Action Module. Takes the structured decision, looks up the tool in the 
    registry, and safely executes the physical code.
    """
    if tool_name in TOOL_REGISTRY:
        try:
            # Unpack dictionary arguments directly into the targeted function
            return TOOL_REGISTRY[tool_name](**arguments)
        except Exception as e:
            return f"ERROR: Exception occurred during action execution: {e}"
    return f"ERROR: Action module could not find registered tool named '{tool_name}'."
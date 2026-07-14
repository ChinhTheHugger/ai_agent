import ollama

MODEL_NAME = 'deepseek-r1'

def request_extraction(system_prompt: str, user_prompt: str) -> str:
    """Asks DeepSeek to parse and structure the incoming user query based on system rules."""
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            format='json'  # Enforces a JSON response at the token level
        )
        return response.message.content
    except Exception as e:
        return f'{{"error": "Failed to connect to Ollama: {str(e)}"}}'

def request_natural_language(system_prompt: str, user_query: str, tool_observation: str) -> str:
    """Asks DeepSeek to convert raw tool data into a polished, human-friendly response."""
    user_context = f"User asked: '{user_query}'\nRaw tool observation: '{tool_observation}'"
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_context}
            ]
        )
        return response.message.content
    except Exception as e:
        return f"Error synthesizing final answer: {e}"
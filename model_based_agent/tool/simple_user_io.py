def ask_user(question: str) -> str:
    """
    Input Action: Interrupts execution, displays a question, 
    and waits for the human to type a response.
    """
    print(f"\n[Agent Clarification Request]: {question}")
    user_response = input("Your Answer: ").strip()
    return user_response

def response_user(message: str) -> str:
    """
    Output Action: Delivers the finalized natural language response 
    to the human user.
    """
    print(f"\n[Agent Final Answer]: {message}")
    return "SUCCESS: Message delivered to user."
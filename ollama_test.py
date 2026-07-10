from ollama import chat

response = chat(
    model='deepseek-r1',
    messages=[{'role': 'user', 'content': 'Testing Ollama Python library...'}],
)
print(response.message.content)
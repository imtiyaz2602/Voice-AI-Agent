from voice_agent import agent_response

while True:
    user_input = input("You: ")
    response = agent_response(user_input)
    print("AI:", response)
from agent.voice_agent import agent_response

print("AI: Hello! How can I help you today?")

while True:
    user = input("You: ")

    if user.lower() in ["exit", "quit"]:
        print("AI: Goodbye!")
        break

    response = agent_response(user)

    print("AI:", response)
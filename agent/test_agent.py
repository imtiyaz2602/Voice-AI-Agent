from agent.voice_agent import agent_response


print("AI: Hello! How can I help you today?")

while True:

    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("AI: Goodbye!")
        break

    response = agent_response(user_input)

    print("AI:", response)
from voice_agent import VoiceAgent

def main():
    print("🤖 Memory Chatbot (type 'exit' to quit)\n")

    user_id = "demo_user"

    agent = VoiceAgent(
        user_id=user_id,
        groq_api_key="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"
    )

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Bot: Bye! 👋")
            break

        try:
            response = agent.process_turn(user_input)
            print("Bot:", response)
        except Exception as e:
            print("Bot: Error:", e)

if __name__ == "__main__":
    main()

from voice_agent import VoiceAgent

agent = VoiceAgent(
    user_id="user123",
    groq_api_key="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"
)

print(agent.process_turn("Hello, remember my favorite color is blue"))




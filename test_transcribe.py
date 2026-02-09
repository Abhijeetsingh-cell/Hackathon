from voice_chatbot import transcribe  # or just use the function if in same file

audio_file = "test_audio.wav"
text = transcribe(audio_file)
print("Transcribed text:", text)

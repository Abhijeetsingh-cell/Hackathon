import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf
import numpy as np
import librosa
import whisper

# === Load Whisper model once ===
whisper_model = whisper.load_model("base")  # or "small", "medium", etc.

# === Function to record audio from mic ===
def record_audio(filename="user_input.wav", duration=5, fs=16000):
    """
    Records audio from the microphone and saves it as WAV.
    """
    print(f"\nRecording for {duration} seconds...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()
    write(filename, fs, (audio * 32767).astype('int16'))
    print(f"Saved recording to {filename}")
    return filename

# === Transcribe function with dtype fix ===
def transcribe(filename):
    """
    Transcribes a WAV audio file using Whisper (float32 fix included)
    """
    import soundfile as sf
    import numpy as np
    import whisper
    # Load audio
    audio, sr = sf.read(filename)

    # Convert stereo to mono
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)

    # Convert to float32
    audio = audio.astype(np.float32)

    # Resample if necessary
 

    # Transcribe
    result = whisper_model.transcribe(mel)
    return result["text"]

# === Main voice chat loop ===
if __name__ == "__main__":
    print("Voice chat started. Say 'exit' to quit.")

    while True:
        # Record audio
        audio_file = record_audio(duration=5)

        # Transcribe
        user_text = transcribe(audio_file)
        print("User said:", user_text)

        # Exit condition
        if user_text.lower().strip() == "exit":
            print("Exiting voice chat.")
            break





import whisper
from pathlib import Path

# Load model
model = whisper.load_model("base")

# Paths
audio_path = Path(r"C:\Users\AMEERAH ADISA\Desktop\audio-to-notes-app\project\audio_input\december.mp3")
output_path = Path(r"raw_transcripts/sample.txt")

# Transcribe
result = model.transcribe(str(audio_path))

# Save transcript
output_path.parent.mkdir(exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Transcription complete.")

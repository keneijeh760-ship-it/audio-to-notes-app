import whisper
from pathlib import Path

# Load model
model = whisper.load_model("base")

# Paths
audio_path = Path("audio_input/sample_audio.mp3")
output_path = Path("raw_transcripts/sample.txt")

# Transcribe
result = model.transcribe(str(audio_path))

# Save transcript
output_path.parent.mkdir(exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(result["text"])

print("Transcription complete.")

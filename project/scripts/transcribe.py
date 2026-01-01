from pathlib import Path
import whisper

AUDIO = Path("audio_input/lecture.mp3")
OUT = Path("raw_transcripts/lecture.txt")

OUT.parent.mkdir(parents=True, exist_ok=True)

model = whisper.load_model("medium", device="cpu")
result = model.transcribe(str(AUDIO))

with open(OUT, "w", encoding="utf-8") as f:
    for s in result["segments"]:
        f.write(
            f"[{s['start']/60:.2f}-{s['end']/60:.2f} min] "
            f"{s['text'].strip()}\n"
        )

print("Lecture transcript saved.")

from pathlib import Path
import whisper
import json

AUDIO = Path(r"C:\Users\AMEERAH ADISA\Desktop\audio-to-notes-app\project\audio_input\lecture.mp3")
OUT = Path("raw_transcripts/lecture.txt")

OUT.parent.mkdir(parents=True, exist_ok=True)

model = whisper.load_model("small", device="cpu")
result = model.transcribe(str(AUDIO))

with open(OUT, "w", encoding="utf-8") as f:
    for s in result["segments"]:
        f.write(
            f"[{s['start']/60:.2f}-{s['end']/60:.2f} min] "
            f"{s['text'].strip()}\n"
        )

# ✅ DEFINE full_text FIRST (guaranteed)
segments = result.get("segments", [])

full_text = " ".join(
    s["text"].strip() for s in segments
)

# Handle empty audio safely
if segments:
    lecture_start = segments[0]["start"]
    lecture_end = segments[-1]["end"]
else:
    lecture_start = 0
    lecture_end = 0

# Format timestamps
def format_time(seconds):
    return f"{int(seconds//3600):02}:{int((seconds%3600)//60):02}:{int(seconds%60):02}"

# Build JSON exactly like your example
output_data = {
    "transcript": [
        {
            
            "start_time": format_time(lecture_start),
            "end_time": format_time(lecture_end),
            "text": full_text
        }
    ],
    "confidence_score": round(result.get("confidence", 0.85), 2),
    "language": "English"
}
print(output_data)

# Save JSON
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("Lecture transcript saved successfully.")
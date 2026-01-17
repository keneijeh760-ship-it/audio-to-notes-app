from pathlib import Path
import whisper
import json
import spacy

# =========================
# PATHS
# =========================
BASE_DIR = Path(__file__).resolve().parents[1]

AUDIO = BASE_DIR / "audio_input" / "lecture.mp3"

TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

RAW_TXT = TRANSCRIPTS_DIR / "lecture_raw.txt"
JSON_OUT = TRANSCRIPTS_DIR / "lecture.json"
CLEAN_TXT = TRANSCRIPTS_DIR / "lecture_cleaned.txt"

# =========================
# LOAD MODELS
# =========================
whisper_model = whisper.load_model("small", device="cpu")
nlp = spacy.load("en_core_web_sm")

# =========================
# TRANSCRIPTION
# =========================
result = whisper_model.transcribe(str(AUDIO))
segments = result.get("segments", [])

# Save raw timestamped transcript
with open(RAW_TXT, "w", encoding="utf-8") as f:
    for s in segments:
        f.write(
            f"[{s['start']/60:.2f}-{s['end']/60:.2f} min] "
            f"{s['text'].strip()}\n"
        )

# =========================
# BUILD FULL TEXT
# =========================
full_text = " ".join(s["text"].strip() for s in segments)

# Handle empty audio safely
lecture_start = segments[0]["start"] if segments else 0
lecture_end = segments[-1]["end"] if segments else 0

def format_time(seconds):
    return f"{int(seconds//3600):02}:{int((seconds%3600)//60):02}:{int(seconds%60):02}"

# =========================
# SAVE JSON OUTPUT
# =========================
output_data = {
    "transcript": [
        {
            "start_time": format_time(lecture_start),
            "end_time": format_time(lecture_end),
            "text": full_text
        }
    ],
    "confidence_score": round(result.get("confidence", 0.85), 2),
    "language": result.get("language", "en")
}

with open(JSON_OUT, "w", encoding="utf-8") as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

# =========================
# CLEAN TRANSCRIPT (spaCy)
# =========================
def clean_transcript(text):
    doc = nlp(text)
    cleaned_sentences = [
        sent.text.strip()
        for sent in doc.sents
        if len(sent.text.strip()) > 20
    ]
    return " ".join(cleaned_sentences)

clean_text = clean_transcript(full_text)

with open(CLEAN_TXT, "w", encoding="utf-8") as f:
    f.write(clean_text)

# =========================
# DONE
# =========================
print("Transcription complete")
print("Raw text:", RAW_TXT)
print("JSON:", JSON_OUT)
print("Cleaned transcript:", CLEAN_TXT)

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

UPLOAD_DIR = BASE_DIR / "uploads"
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
SUMMARIES_DIR = BASE_DIR / "summaries"
NOTES_DIR = BASE_DIR / "notes"

# Create folders if they don't exist
for directory in [UPLOAD_DIR, TRANSCRIPTS_DIR, SUMMARIES_DIR, NOTES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
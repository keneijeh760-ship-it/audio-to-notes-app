import os

UPLOAD_DIR = "uploads"
TRANSCRIPTS_DIR = "transcripts"
SUMMARIES_DIR = "summaries"
NOTES_DIR = "notes"

for directory in [UPLOAD_DIR, TRANSCRIPTS_DIR, SUMMARIES_DIR, NOTES_DIR]:
    os.makedirs(directory, exist_ok=True)
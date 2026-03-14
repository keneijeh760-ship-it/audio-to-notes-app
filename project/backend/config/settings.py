from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# ===============================
# Project paths
# ===============================

BASE_DIR = Path(__file__).resolve().parents[1]

UPLOAD_DIR = BASE_DIR / "uploads"
TRANSCRIPTS_DIR = BASE_DIR / "transcripts"
SUMMARIES_DIR = BASE_DIR / "summaries"
NOTES_DIR = BASE_DIR / "notes"

# Create folders if they don't exist
for directory in [UPLOAD_DIR, TRANSCRIPTS_DIR, SUMMARIES_DIR, NOTES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ===============================
# Supabase configuration
# ===============================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

AUDIO_BUCKET = os.getenv("SUPABASE_BUCKET_AUDIO")
TRANSCRIPT_BUCKET = os.getenv("SUPABASE_BUCKET_TRANSCRIPTS")
SUMMARY_BUCKET = os.getenv("SUPABASE_BUCKET_SUMMARIES")

# ===============================
# Model settings
# ===============================

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

# ===============================
# API configuration
# ===============================

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
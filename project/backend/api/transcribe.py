#Engineer 3 connect whisper

from fastapi import APIRouter, HTTPException
import json
import os
import uuid
from datetime import datetime
from project.backend.models.schemas import TranscribeRequest
from project.backend.storage.file_manager import TRANSCRIPTS_DIR


router = APIRouter()

def generate_id():
    return str(uuid.uuid4())

def get_timestamp():
    return datetime.now().isoformat()

@router.post("/transcribe")
def transcribe_audio(request: TranscribeRequest):

    transcript_id = generate_id()

    transcript_data = {
        "transcript_id": transcript_id,
        "audio_file_id": request.audio_file_id,
        "transcript_text": "Simulated transcript",
        "timestamp": get_timestamp()
    }

    transcript_file = os.path.join(
        TRANSCRIPTS_DIR,
        f"{transcript_id}.json"
    )

    with open(transcript_file, "w") as f:
        json.dump(transcript_data, f, indent=2)

    return {
        "success": True,
        "data": transcript_data
    }
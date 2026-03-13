#Engineer 4, integrate the NLP summarizer


from fastapi import APIRouter, HTTPException
import json
import os
import uuid
from datetime import datetime
from project.backend.models.schemas import SummarizeRequest
from project.backend.storage.file_manager import TRANSCRIPTS_DIR, SUMMARIES_DIR


router = APIRouter()

def generate_id():
    return str(uuid.uuid4())

def get_timestamp():
    return datetime.now().isoformat()

@router.post("/summarize")
def summarize_transcript(request: SummarizeRequest):

    transcript_file = os.path.join(
        TRANSCRIPTS_DIR,
        f"{request.transcript_id}.json"
    )

    if not os.path.exists(transcript_file):
        raise HTTPException(status_code=404, detail="Transcript not found")

    with open(transcript_file) as f:
        transcript = json.load(f)

    summary_id = generate_id()

    summary_data = {
        "summary_id": summary_id,
        "transcript_id": request.transcript_id,
        "summary_text": "Simulated summary",
        "timestamp": get_timestamp()
    }

    summary_file = os.path.join(SUMMARIES_DIR, f"{summary_id}.json")

    with open(summary_file, "w") as f:
        json.dump(summary_data, f, indent=2)

    return {
        "success": True,
        "data": summary_data
    }
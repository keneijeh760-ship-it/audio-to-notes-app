#Engineer 5 implement the logic.

from fastapi import APIRouter
import json
import os
import uuid
from datetime import datetime
from project.backend.models.schemas import SaveNotesRequest
from project.backend.storage.file_manager import NOTES_DIR


router = APIRouter()

def generate_id():
    return str(uuid.uuid4())

def get_timestamp():
    return datetime.now().isoformat()

@router.post("/save-notes")
def save_notes(request: SaveNotesRequest):

    note_id = generate_id()

    notes_data = {
        "note_id": note_id,
        "transcript_id": request.transcript_id,
        "summary_id": request.summary_id,
        "created_at": get_timestamp(),
        "user_notes": request.user_notes
    }

    note_file = os.path.join(NOTES_DIR, f"{note_id}.json")

    with open(note_file, "w") as f:
        json.dump(notes_data, f, indent=2)

    return {
        "success": True,
        "data": notes_data
    }
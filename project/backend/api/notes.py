from fastapi import APIRouter
import uuid
from datetime import datetime
from project.backend.models.schemas import SaveNotesRequest
from project.backend.supabase_service import supabase

router = APIRouter()

@router.post("/save-notes")
def save_notes(request: SaveNotesRequest):

    note_id = str(uuid.uuid4())

    data = {
        "id": note_id,
        "transcript_id": request.transcript_id,
        "summary_id": request.summary_id,
        "user_notes": request.user_notes,
        "created_at": datetime.utcnow().isoformat()
    }

    supabase.table("notes").insert(data).execute()

    return {"success": True, "data": data}


@router.get("/notes")
def get_notes():
    notes = supabase.table("notes").select("*").execute()
    return {"success": True, "data": notes.data}


@router.get("/notes/{note_id}")
def get_note(note_id: str):
    note = supabase.table("notes").select("*").eq("id", note_id).execute()
    return {"success": True, "data": note.data}
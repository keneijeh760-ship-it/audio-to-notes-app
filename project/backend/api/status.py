from fastapi import APIRouter
from project.backend.supabase_service import supabase

router = APIRouter()

@router.get("/status/{file_id}")
def get_status(file_id: str):

    status = {
        "uploaded": False,
        "transcribed": False,
        "summarized": False,
        "saved": False
    }

    # ✅ Check upload
    upload = supabase.table("uploads").select("*").eq("id", file_id).execute()
    if upload.data:
        status["uploaded"] = True

    # ✅ Check transcription
    transcript = supabase.table("transcripts").select("*").eq("upload_id", file_id).execute()
    if transcript.data:
        status["transcribed"] = True
        transcript_id = transcript.data[0]["id"]
    else:
        transcript_id = None

    # ✅ Check summary
    if transcript_id:
        summary = supabase.table("summaries").select("*").eq("transcript_id", transcript_id).execute()
        if summary.data:
            status["summarized"] = True
            summary_id = summary.data[0]["id"]
        else:
            summary_id = None
    else:
        summary_id = None

    # ✅ Check notes
    if summary_id:
        notes = supabase.table("notes").select("*").eq("summary_id", summary_id).execute()
        if notes.data:
            status["saved"] = True

    return {
        "file_id": file_id,
        "status": status
    }
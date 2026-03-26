from fastapi import APIRouter, HTTPException
import uuid
import requests
import tempfile
import whisper
from datetime import datetime

from project.backend.models.schemas import TranscribeRequest
from project.backend.supabase_service import supabase
from project.backend.services.metrics_service import update_metrics

router = APIRouter()

model = whisper.load_model("base")

@router.post("/transcribe")
def transcribe_audio(request: TranscribeRequest):

    upload = supabase.table("uploads").select("*").eq("id", request.audio_file_id).execute()

    if not upload.data:
        raise HTTPException(404, "Upload not found")

    file_url = upload.data[0]["file_url"]

    # download file
    audio = requests.get(file_url).content
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio)
        temp_path = f.name

    result = model.transcribe(temp_path)

    transcript_id = str(uuid.uuid4())

    text = result["text"]
    word_count = len(text.split())

    supabase.table("transcripts").insert({
        "id": transcript_id,
        "upload_id": request.audio_file_id,
        "transcript_text": text,
        "duration_seconds": result.get("duration", 0),
        "confidence": 0.9,
        "word_count": word_count,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

    update_metrics("total_transcriptions", 1)
    update_metrics("total_words_transcribed", word_count)

    # update status
    supabase.table("uploads").update({
        "status": "transcribed"
    }).eq("id", request.audio_file_id).execute()

    return {
        "success": True,
        "transcript_id": transcript_id,
        "text": result["text"]
    }
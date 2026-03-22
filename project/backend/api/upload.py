from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid
from datetime import datetime
from project.backend.supabase_service import supabase
from project.backend.config.settings import AUDIO_BUCKET
from project.backend.services.metrics_service import update_metrics

router = APIRouter()

@router.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    allowed = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
    
    if not any(file.filename.endswith(ext) for ext in allowed):
        raise HTTPException(400, "Invalid file type")

    file_id = str(uuid.uuid4())
    file_bytes = await file.read()

    path = f"{file_id}_{file.filename}"

    # Upload to Supabase storage
    supabase.storage.from_(AUDIO_BUCKET).upload(path, file_bytes)

    file_url = supabase.storage.from_(AUDIO_BUCKET).get_public_url(path)

    # Insert metadata
    supabase.table("uploads").insert({
        "id": file_id,
        "filename": file.filename,
        "file_url": file_url,
        "file_size": len(file_bytes),
        "status": "uploaded",
        "upload_time": datetime.utcnow().isoformat()
    }).execute()

    update_metrics("total_uploads", 1)

    return {
        "success": True,
        "file_id": file_id,
        "file_url": file_url
    }
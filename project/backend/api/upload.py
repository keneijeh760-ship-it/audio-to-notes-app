#Engineer 2

from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import uuid
from datetime import datetime
from project.backend.storage.file_manager import UPLOAD_DIR


router = APIRouter()

processing_status = {}

def generate_id():
    return str(uuid.uuid4())

def get_timestamp():
    return datetime.now().isoformat()

@router.post("/upload-audio")
def upload_audio(file: UploadFile = File(...)):
    
    allowed_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
    file_ext = os.path.splitext(file.filename)[1].lower()

    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_id = generate_id()
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")

    content = file.file.read()

    with open(file_path, "wb") as f:
        f.write(content)

    processing_status[file_id] = {
        "status": "uploaded",
        "filename": file.filename,
        "upload_timestamp": get_timestamp()
    }

    return {
        "success": True,
        "file_id": file_id
    }
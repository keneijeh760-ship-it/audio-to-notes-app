from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class TranscribeRequest(BaseModel):
    audio_file_id: str
    language: Optional[str] = "en"

class SummarizeRequest(BaseModel):
    transcript_id: str

class SaveNotesRequest(BaseModel):
    transcript_id: str
    summary_id: str
    user_notes: Optional[str] = ""

class APIResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
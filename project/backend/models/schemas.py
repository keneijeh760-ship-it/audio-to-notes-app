#Engineer 6

from pydantic import BaseModel
from typing import Optional, Dict, Any

class TranscribeRequest(BaseModel):
    audio_file_id: str
    language: Optional[str] = "en"

class SummarizeRequest(BaseModel):
    transcript_id: str
    summary_type: Optional[str] = "standard"

class SaveNotesRequest(BaseModel):
    transcript_id: str
    summary_id: str
    user_notes: Optional[str] = ""

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
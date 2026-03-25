"""
Backend API for Audio Transcription and Note-Taking System
FastAPI implementation - Python 3.13 Compatible Version
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

security = HTTPBearer()

# Initialize FastAPI app
app = FastAPI(
    title="Audio Transcription API",
    description="Backend API for managing audio transcription and note summarization",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data storage directories
UPLOAD_DIR = "uploads"
TRANSCRIPTS_DIR = "transcripts"
SUMMARIES_DIR = "summaries"
NOTES_DIR = "notes"

# Create directories if they don't exist
for directory in [UPLOAD_DIR, TRANSCRIPTS_DIR, SUMMARIES_DIR, NOTES_DIR]:
    os.makedirs(directory, exist_ok=True)

# In-memory storage for demo purposes
processing_status = {}

# Pydantic models for request/response validation
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

class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Verify the Bearer token with Supabase and return the user object."""
    token = credentials.credentials
    try:
        user_response = supabase.auth.get_user(token)
        return {"id": user_response.user.id, "email": user_response.user.email}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# Utility functions
def generate_id():
    """Generate unique ID for resources"""
    return str(uuid.uuid4())

def get_timestamp():
    """Get current timestamp"""
    return datetime.now().isoformat()

def simulate_asr_processing(audio_file_id: str) -> Dict[str, Any]:
    """Simulate ASR (Automatic Speech Recognition) processing"""
    return {
        "transcript_id": generate_id(),
        "audio_file_id": audio_file_id,
        "transcript_text": "This is a simulated transcript of the audio recording. In a real implementation, this would be the output from an ASR service like Whisper, Google Speech-to-Text, or Azure Speech Services.",
        "duration_seconds": 120,
        "language": "en",
        "confidence": 0.95,
        "timestamp": get_timestamp(),
        "metadata": {
            "speaker_count": 1,
            "audio_quality": "high"
        }
    }

def simulate_nlp_processing(transcript_text: str) -> Dict[str, Any]:
    """Simulate NLP (Natural Language Processing) for summarization"""
    return {
        "summary_id": generate_id(),
        "summary_text": "Summary: This recording covers key concepts and important points. Main topics discussed include fundamental principles and practical applications.",
        "key_points": [
            "First key point extracted from the transcript",
            "Second important concept discussed",
            "Third major takeaway from the content"
        ],
        "entities": ["concept", "principle", "application"],
        "sentiment": "neutral",
        "timestamp": get_timestamp()
    }


# API Endpoints

@app.get("/")
def root():
    """Root endpoint - API health check"""
    return {
        "message": "Audio Transcription API is running",
        "version": "1.0.0",
        "status": "healthy",
        "endpoints": {
            "auth_signup": "/auth/signup",
            "auth_login": "/auth/login",
            "auth_logout": "/auth/logout",
            "upload": "/upload-audio",
            "transcribe": "/transcribe",
            "summarize": "/summarize",
            "save": "/save-notes",
            "retrieve": "/notes/{note_id}"
        }
    }


@app.post("/auth/signup")
def auth_signup(request: SignUpRequest):
    """Register a new user with name, email, and password."""
    try:
        response = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {"data": {"name": request.name}},
        })

        if response.user is None:
            return JSONResponse(
                status_code=400,
                content={"success": False, "message": "Sign-up failed", "error": "Could not create user"},
            )

        session = response.session
        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "name": request.name,
                    "access_token": session.access_token if session else None,
                },
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": "Sign-up failed", "error": str(e)},
        )


@app.post("/auth/login")
def auth_login(request: LoginRequest):
    """Authenticate a user with email and password."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password,
        })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Login successful",
                "data": {
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "name": response.user.user_metadata.get("name", ""),
                    "access_token": response.session.access_token,
                },
            },
        )
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={"success": False, "message": "Login failed", "error": str(e)},
        )


@app.post("/auth/logout")
def auth_logout(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Log out the current user."""
    try:
        supabase.auth.sign_out()
        return JSONResponse(
            status_code=200,
            content={"success": True, "message": "Logged out successfully"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Logout failed", "error": str(e)},
        )


@app.post("/upload-audio")
def upload_audio(file: UploadFile = File(...), current_user: Dict[str, Any] = Depends(get_current_user)):
    """Accept audio file upload from frontend"""
    try:
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.ogg', '.flac']
        file_ext = os.path.splitext(file.filename)[1].lower()

        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file format. Allowed formats: {', '.join(allowed_extensions)}"
            )

        file_id = generate_id()
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}{file_ext}")

        content = file.file.read()
        with open(file_path, 'wb') as f:
            f.write(content)

        processing_status[file_id] = {
            "user_id": current_user["id"],
            "status": "uploaded",
            "filename": file.filename,
            "file_size": len(content),
            "upload_timestamp": get_timestamp()
        }

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Audio file uploaded successfully",
                "data": {
                    "file_id": file_id,
                    "filename": file.filename,
                    "file_size_bytes": len(content),
                    "format": file_ext,
                    "upload_timestamp": get_timestamp()
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Failed to upload audio file",
                "error": str(e)
            }
        )

@app.post("/transcribe")
def transcribe_audio(request: TranscribeRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Send audio to ASR module for transcription"""
    try:
        if request.audio_file_id not in processing_status:
            raise HTTPException(status_code=404, detail="Audio file not found. Please upload the file first.")

        if processing_status[request.audio_file_id].get("user_id") != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")

        asr_output = simulate_asr_processing(request.audio_file_id)
        asr_output["user_id"] = current_user["id"]

        transcript_file = os.path.join(TRANSCRIPTS_DIR, f"{asr_output['transcript_id']}.json")
        with open(transcript_file, 'w') as f:
            json.dump(asr_output, f, indent=2)

        processing_status[request.audio_file_id]["status"] = "transcribed"
        processing_status[request.audio_file_id]["transcript_id"] = asr_output["transcript_id"]

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Audio transcribed successfully",
                "data": asr_output
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Transcription failed",
                "error": str(e)
            }
        )

@app.post("/summarize")
def summarize_transcript(request: SummarizeRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Send transcript to NLP module for summarization"""
    try:
        transcript_file = os.path.join(TRANSCRIPTS_DIR, f"{request.transcript_id}.json")

        if not os.path.exists(transcript_file):
            raise HTTPException(status_code=404, detail="Transcript not found. Please transcribe the audio first.")

        with open(transcript_file, 'r') as f:
            transcript_data = json.load(f)

        if transcript_data.get("user_id") != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")

        nlp_output = simulate_nlp_processing(transcript_data["transcript_text"])
        nlp_output["transcript_id"] = request.transcript_id
        nlp_output["user_id"] = current_user["id"]

        summary_file = os.path.join(SUMMARIES_DIR, f"{nlp_output['summary_id']}.json")
        with open(summary_file, 'w') as f:
            json.dump(nlp_output, f, indent=2)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Transcript summarized successfully",
                "data": nlp_output
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Summarization failed",
                "error": str(e)
            }
        )

@app.post("/save-notes")
def save_notes(request: SaveNotesRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Store final processed output and summarized notes"""
    try:
        transcript_file = os.path.join(TRANSCRIPTS_DIR, f"{request.transcript_id}.json")
        with open(transcript_file, 'r') as f:
            transcript_data = json.load(f)

        if transcript_data.get("user_id") != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")

        summary_file = os.path.join(SUMMARIES_DIR, f"{request.summary_id}.json")
        with open(summary_file, 'r') as f:
            summary_data = json.load(f)

        if summary_data.get("user_id") != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")

        note_id = generate_id()
        notes_document = {
            "note_id": note_id,
            "user_id": current_user["id"],
            "transcript_id": request.transcript_id,
            "summary_id": request.summary_id,
            "created_at": get_timestamp(),
            "transcript": transcript_data,
            "summary": summary_data,
            "user_notes": request.user_notes,
            "status": "saved"
        }

        notes_file = os.path.join(NOTES_DIR, f"{note_id}.json")
        with open(notes_file, 'w') as f:
            json.dump(notes_document, f, indent=2)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Notes saved successfully",
                "data": {
                    "note_id": note_id,
                    "created_at": notes_document["created_at"],
                    "transcript_length": len(transcript_data.get("transcript_text", "")),
                    "summary_points": len(summary_data.get("key_points", [])),
                    "has_user_notes": bool(request.user_notes)
                }
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Failed to save notes",
                "error": str(e)
            }
        )

@app.get("/notes/{note_id}")
def get_notes(note_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Retrieve saved notes by ID"""
    try:
        notes_file = os.path.join(NOTES_DIR, f"{note_id}.json")

        if not os.path.exists(notes_file):
            raise HTTPException(status_code=404, detail="Notes not found")

        with open(notes_file, 'r') as f:
            notes_data = json.load(f)

        if notes_data.get("user_id") != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied")

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Notes retrieved successfully",
                "data": notes_data
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Failed to retrieve notes",
                "error": str(e)
            }
        )

@app.get("/notes")
def list_all_notes(current_user: Dict[str, Any] = Depends(get_current_user)):
    """List all saved notes for the current user"""
    try:
        notes_list = []

        for filename in os.listdir(NOTES_DIR):
            if filename.endswith('.json'):
                file_path = os.path.join(NOTES_DIR, filename)
                with open(file_path, 'r') as f:
                    note_data = json.load(f)
                    if note_data.get("user_id") != current_user["id"]:
                        continue
                    notes_list.append({
                        "note_id": note_data["note_id"],
                        "created_at": note_data["created_at"],
                        "has_user_notes": bool(note_data.get("user_notes"))
                    })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": f"Found {len(notes_list)} notes",
                "data": {
                    "count": len(notes_list),
                    "notes": notes_list
                }
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Failed to list notes",
                "error": str(e)
            }
        )

@app.get("/status/{file_id}")
def get_processing_status(file_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    """Check processing status of an uploaded file"""
    if file_id not in processing_status:
        raise HTTPException(status_code=404, detail="File not found")

    if processing_status[file_id].get("user_id") != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied")

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Status retrieved successfully",
            "data": processing_status[file_id]
        }
    )

# Error handlers
@app.exception_handler(404)
def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "message": "Resource not found",
            "error": str(exc.detail) if hasattr(exc, 'detail') else "Not found"
        }
    )

@app.exception_handler(500)
def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "error": "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

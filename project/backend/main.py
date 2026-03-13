from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from project.backend.api.upload import router as upload_router
from project.backend.api.transcribe import router as transcribe_router
from project.backend.api.summarize import router as summarize_router
from project.backend.api.notes import router as notes_router

app = FastAPI(
    title="Audio Notes API",
    description="Audio transcription and note summarization system",
    version="1.0"
)

# CORS (frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "Audio Notes API is running",
        "version": "1.0",
        "status": "healthy"
    }

@app.get("/routes")
def routes():
    return [route.path for route in app.routes]


# Connect routers
app.include_router(upload_router)
app.include_router(transcribe_router)
app.include_router(summarize_router)
app.include_router(notes_router)
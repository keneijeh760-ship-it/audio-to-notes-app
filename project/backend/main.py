from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from project.backend.api.upload import router as upload_router
from project.backend.api.transcribe import router as transcribe_router
from project.backend.api.summarize import router as summarize_router
from project.backend.api.notes import router as notes_router
from project.backend.api.status import router as status_router
from project.backend.api.metrics import router as metrics_router


app = FastAPI(title="Audio Notes API", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": str(exc)}
    )

@app.get("/")
def root():
    return {
        "success": True,
        "message": "API Running",
        "services": ["upload", "transcribe", "summarize", "notes"]
    }

# Routers
app.include_router(upload_router)
app.include_router(transcribe_router)
app.include_router(summarize_router)
app.include_router(notes_router)
app.include_router(status_router)
app.include_router(metrics_router)
from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime
import os
from groq import Groq

from project.backend.models.schemas import SummarizeRequest
from project.backend.supabase_service import supabase

router = APIRouter()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@router.post("/summarize")
def summarize(request: SummarizeRequest):

    transcript = supabase.table("transcripts").select("*").eq("id", request.transcript_id).execute()

    if not transcript.data:
        raise HTTPException(404, "Transcript not found")

    text = transcript.data[0]["transcript_text"]

    # 🔥 Groq AI summarization
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an expert note-taking assistant. Summarize clearly into concise bullet points."
            },
            {
                "role": "user",
                #"content": f"Summarize this transcript into clear notes:\n\n{text}"
                "content": f"Summarize this transcript into 5-7 concise bullet points. Keep it under 120 words. Focus only on key ideas:\n\n{text}"
            }
        ],
        temperature=0.3
    )

    summary = response.choices[0].message.content

    word_count = len(summary.split())

    summary_id = str(uuid.uuid4())

    supabase.table("summaries").insert({
        "id": summary_id,
        "transcript_id": request.transcript_id,
        "summary_text": summary,
        "key_points": [],
        "entities": [],
        "word_count": word_count,
        "created_at": datetime.utcnow().isoformat()
    }).execute()

    return {
        "success": True,
        "summary_id": summary_id,
        "summary": summary,
        "word_count": word_count
    }
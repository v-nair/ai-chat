from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAIError
from dotenv import load_dotenv
import logging
import os

from models import ChatRequest, ChatResponse
from services.chat_service import send_message, clear_session

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables")

app = FastAPI(
    title="AI Chat API",
    description="Conversational AI backend with session memory powered by GPT-4o",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ai-chat-api is running"}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(req: ChatRequest):
    try:
        reply = send_message(req.session_id, req.message)
    except OpenAIError:
        raise HTTPException(status_code=502, detail="AI service unavailable")
    return ChatResponse(reply=reply, session_id=req.session_id)


@app.delete("/chat/{session_id}", tags=["Chat"])
def delete_session(session_id: str):
    if not clear_session(session_id):
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "session cleared", "session_id": session_id}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in environment variables")

client = OpenAI(api_key=api_key)

conversations: dict[str, list[dict]] = {}

SYSTEM_PROMPT = "You are a helpful assistant."
MAX_HISTORY = 20


class ChatRequest(BaseModel):
    session_id: str
    message: str

    @field_validator("session_id", "message")
    @classmethod
    def must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field must not be empty")
        return v.strip()


class ChatResponse(BaseModel):
    reply: str
    session_id: str


@app.get("/", tags=["Health"])
def root():
    return {"status": "ai-chat-api is running"}


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
def chat(req: ChatRequest):
    if req.session_id not in conversations:
        conversations[req.session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    conversations[req.session_id].append({
        "role": "user",
        "content": req.message
    })

    history = conversations[req.session_id]
    if len(history) > MAX_HISTORY + 1:
        conversations[req.session_id] = [history[0]] + history[-(MAX_HISTORY):]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=conversations[req.session_id],
            temperature=0.7,
            max_tokens=1000,
        )
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=502, detail="AI service unavailable")

    reply = response.choices[0].message.content

    conversations[req.session_id].append({
        "role": "assistant",
        "content": reply
    })

    logger.info(f"Session {req.session_id}: {len(conversations[req.session_id])} messages")

    return ChatResponse(reply=reply, session_id=req.session_id)


@app.delete("/chat/{session_id}", tags=["Chat"])
def clear_session(session_id: str):
    if session_id not in conversations:
        raise HTTPException(status_code=404, detail="Session not found")
    conversations.pop(session_id)
    return {"status": "session cleared", "session_id": session_id}

from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# In-memory conversation store
conversations: dict[str, list] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    session_id: str

@app.get("/")
def root():
    return {"status": "ai-chat-api is running"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if req.session_id not in conversations:
        conversations[req.session_id] = [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            }
        ]

    conversations[req.session_id].append({
        "role": "user",
        "content": req.message
    })

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversations[req.session_id]
    )

    reply = response.choices[0].message.content

    conversations[req.session_id].append({
        "role": "assistant",
        "content": reply
    })

    return ChatResponse(reply=reply, session_id=req.session_id)

@app.delete("/chat/{session_id}")
def clear_session(session_id: str):
    conversations.pop(session_id, None)
    return {"status": "session cleared"}

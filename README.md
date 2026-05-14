# AI Chat

A full-stack conversational AI application with multi-turn session memory, built with FastAPI and React.

## Architecture

```text
React UI (Vite)          FastAPI Backend              OpenAI
     │                         │                         │
     │  POST /chat             │                         │
     │ ──────────────────────► │                         │
     │  {session_id, message}  │  chat.completions       │
     │                         │ ──────────────────────► │
     │                         │  GPT-4o response        │
     │  {reply, session_id}    │ ◄────────────────────── │
     │ ◄────────────────────── │                         │
```

Session history is maintained in-memory per `session_id`, trimmed to a rolling window of 20 messages to stay within token limits.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Backend | FastAPI, Python 3.11, Uvicorn |
| AI | OpenAI GPT-4o (`gpt-4o`) |
| Frontend | React 19, Vite, Axios |
| Infrastructure | Docker, Docker Compose |

## Project Structure

```text
ai-chat/
├── ai-chat-api/
│   ├── app/
│   │   ├── main.py                  # FastAPI app, middleware, routes
│   │   ├── models.py                # Pydantic request/response models
│   │   ├── config.py                # Model name, history limits, system prompt
│   │   └── services/
│   │       └── chat_service.py      # Session management, OpenAI calls
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
└── ai-chat-ui/
    └── src/
        └── App.jsx                  # Chat UI with useState, axios
```

## Running Locally

**Prerequisites:** Docker, Node.js, OpenAI API key

**Backend:**

```bash
cd ai-chat-api
cp .env.example .env        # paste your OPENAI_API_KEY
docker compose up --build
```

**Frontend:**

```bash
cd ai-chat-ui
npm install
npm run dev
```

| Service | URL |
| --- | --- |
| API | <http://localhost:8000> |
| Interactive API docs | <http://localhost:8000/docs> |
| UI | <http://localhost:5173> |

## API Reference

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `POST` | `/chat` | Send a message, receive a reply |
| `DELETE` | `/chat/{session_id}` | Clear a session's history |

**POST /chat — request:**

```json
{
  "session_id": "user-abc123",
  "message": "Explain how transformers work"
}
```

**POST /chat — response:**

```json
{
  "reply": "Transformers are...",
  "session_id": "user-abc123"
}
```

## What This Demonstrates

- **FastAPI** — routing, Pydantic validation with `field_validator`, middleware, HTTPException
- **Service layer architecture** — business logic isolated from route handlers
- **OpenAI integration** — chat completions API, multi-turn message history
- **Session memory** — rolling context window with overflow protection
- **Dockerized deployment** — backend containerized and served via Uvicorn
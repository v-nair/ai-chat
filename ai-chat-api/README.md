# AI Chat API

Conversational AI backend with multi-turn session memory powered by GPT-4o, built with FastAPI and the OpenAI Python SDK.

## Architecture

```text
React UI
    │
    │  POST /chat
    ▼
FastAPI (main.py)
    │
    ▼
chat_service.py
    ├── In-memory session store  { session_id: [messages] }
    ├── History trimming         (keeps last 20 turns)
    └── OpenAI client (lazy singleton)
    │
    ▼
OpenAI GPT-4o
```

## Tech Stack

| Layer | Technology |
| --- | --- |
| Framework | FastAPI, Python 3.11 |
| LLM | OpenAI GPT-4o |
| OpenAI client | `openai` Python SDK |
| Infrastructure | Docker, Docker Compose |

## Project Structure

```text
ai-chat-api/
├── app/
│   ├── main.py              # FastAPI app, CORS, routes
│   ├── models.py            # ChatRequest, ChatResponse (Pydantic)
│   ├── config.py            # Model name, system prompt, history limit
│   └── services/
│       └── chat_service.py  # Session management, OpenAI calls
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Running Locally

```bash
cp .env.example .env   # add your OPENAI_API_KEY
docker compose up --build
```

API available at <http://localhost:8000> · Swagger docs at <http://localhost:8000/docs>

## API Reference

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `POST` | `/chat` | Send a message and receive a reply |
| `DELETE` | `/chat/{session_id}` | Clear a session's message history |

**POST /chat — request:**

```json
{
  "session_id": "user-abc123",
  "message": "What is the capital of France?"
}
```

**POST /chat — response:**

```json
{
  "reply": "The capital of France is Paris.",
  "session_id": "user-abc123"
}
```

## Logic — Pseudocode

```text
FUNCTION handle_chat(session_id, message):

    IF session_id not in sessions:
        sessions[session_id] = [SystemMessage("You are a helpful assistant")]

    APPEND HumanMessage(message) to sessions[session_id]

    IF len(sessions[session_id]) > MAX_HISTORY + 1:
        TRIM to [system_prompt] + last 20 messages   // preserve system prompt always

    response = OpenAI GPT-4o.complete(sessions[session_id])

    APPEND AIMessage(response) to sessions[session_id]

    RETURN response


FUNCTION clear_session(session_id):
    IF session_id not in sessions: RETURN false
    DELETE sessions[session_id]
    RETURN true
```

## What This Demonstrates

- **FastAPI** — typed routes, Pydantic request/response models, CORS middleware
- **Session memory** — per-session conversation history stored in memory, trimmed to last 20 turns
- **Lazy singleton** — OpenAI client initialised once on first use
- **Service layer** — business logic separated from route handlers
- **Docker** — containerised with bind-mount for hot reload during development

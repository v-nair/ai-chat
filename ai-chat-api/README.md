# ai-chat-api

FastAPI backend service for the [AI Chat](../README.md) project. Receives messages from `ai-chat-ui`, maintains per-session conversation history, and calls OpenAI GPT-4o to generate replies.

## Relationship to Other Services

| Service | Direction | Description |
| --- | --- | --- |
| `ai-chat-ui` | ← receives requests | UI sends `POST /chat` with `session_id` + `message` |
| OpenAI API | → calls | Sends full conversation history, receives GPT-4o reply |

## Service Structure

```text
app/
├── main.py              # FastAPI app, CORS middleware, route handlers
├── models.py            # ChatRequest, ChatResponse (Pydantic)
├── config.py            # MODEL, MAX_HISTORY, SYSTEM_PROMPT constants
└── services/
    └── chat_service.py  # Session store, history trimming, OpenAI client
```

## Configuration

`.env` (copy from `.env.example`):

```text
OPENAI_API_KEY=sk-...
```

`config.py` values:

| Constant | Value | Purpose |
| --- | --- | --- |
| `MODEL` | `gpt-4o` | OpenAI model used for completions |
| `MAX_HISTORY` | `20` | Max conversation turns kept per session |
| `SYSTEM_PROMPT` | `"You are a helpful assistant."` | Initial system instruction |

## Starting This Service

```bash
cp .env.example .env   # add OPENAI_API_KEY
docker compose up --build
```

Runs on `http://localhost:8000` · Swagger docs at `http://localhost:8000/docs`

## Logic — Pseudocode

```text
FUNCTION handle_chat(session_id, message):

    IF session_id not in sessions:
        sessions[session_id] = [SystemMessage(SYSTEM_PROMPT)]

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

## Design Notes

- **Lazy singleton** — OpenAI client is instantiated on first use and reused across requests
- **In-memory store** — sessions live in a plain Python dict; they do not persist across container restarts
- **History trimming** — always keeps `messages[0]` (the system prompt) and the most recent `MAX_HISTORY` turns
- **502 on OpenAI error** — `OpenAIError` is caught at the route level and returns a 502 to the UI

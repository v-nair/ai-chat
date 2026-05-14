# AI Chat UI

React frontend for the AI Chat project. Provides a chat bubble interface that communicates with the FastAPI backend over a REST API.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Framework | React 19, Vite |
| HTTP client | Axios |
| Styling | Inline styles |

## Project Structure

```text
ai-chat-ui/
├── src/
│   ├── main.jsx     # React entry point
│   ├── index.css    # Global styles
│   └── App.jsx      # Chat UI — state, API calls, message rendering
├── index.html
├── vite.config.js
└── package.json
```

## Running Locally

```bash
npm install
npm run dev
```

UI available at <http://localhost:5173> — requires the `ai-chat-api` backend running on port 8000.

## Logic — Pseudocode

```text
ON component mount:
    sessions[session_id] = []   // empty message list

ON user submits message:
    APPEND { role: "user", content: message } to messages
    SET loading = true

    response = POST /chat { session_id, message }

    APPEND { role: "assistant", content: response.reply } to messages
    SET loading = false

RENDER:
    FOR each message in messages:
        IF role == "user":   render right-aligned blue bubble
        IF role == "assistant": render left-aligned grey bubble
    IF loading: render typing indicator
```

## What This Demonstrates

- **React state management** — `useState` for messages, input, and loading
- **Axios** — POST requests with JSON body and async/await
- **Session identity** — random `session_id` generated on mount, sent with every request
- **Conditional rendering** — per-role bubble styling, loading indicator

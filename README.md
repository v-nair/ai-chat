# AI Chat

A full-stack conversational AI application built with FastAPI and React.

## Projects
- `ai-chat-api` — Python/FastAPI backend with GPT-4o and session memory
- `ai-chat-ui` — React frontend with real-time chat interface

## Tech Stack
- **Backend:** FastAPI · Python 3.11 · OpenAI GPT-4o · Docker
- **Frontend:** React · Vite · Axios

## Features
- Multi-turn conversation with session memory
- Input validation and error handling
- Token overflow protection
- Auto-generated API docs at `/docs`
- Fully containerized with Docker

## Run Locally

**Backend:**
```bash
cd ai-chat-api
cp .env.example .env  # add your OpenAI API key
docker-compose up --build
```

**Frontend:**
```bash
cd ai-chat-ui
npm install
npm run dev
```

API runs on `http://localhost:8000`
UI runs on `http://localhost:5173`
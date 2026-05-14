import os
import logging
from openai import OpenAI, OpenAIError

from config import MODEL, MAX_HISTORY, SYSTEM_PROMPT

logger = logging.getLogger(__name__)

_client: OpenAI | None = None
_conversations: dict[str, list[dict]] = {}


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def _get_or_create_session(session_id: str) -> list[dict]:
    if session_id not in _conversations:
        _conversations[session_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
    return _conversations[session_id]


def _trim_history(session_id: str) -> None:
    history = _conversations[session_id]
    if len(history) > MAX_HISTORY + 1:
        _conversations[session_id] = [history[0]] + history[-MAX_HISTORY:]


def send_message(session_id: str, message: str) -> str:
    """Append ``message`` to the session history, call GPT-4o, and return the reply.

    Creates the session if it does not exist and trims history to ``MAX_HISTORY``
    turns while always preserving the system prompt at index 0.
    Raises ``OpenAIError`` on API failure.
    """
    _get_or_create_session(session_id)
    _conversations[session_id].append({"role": "user", "content": message})
    _trim_history(session_id)

    try:
        response = _get_client().chat.completions.create(
            model=MODEL,
            messages=_conversations[session_id],
            temperature=0.7,
            max_tokens=1000,
        )
    except OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise

    reply = response.choices[0].message.content
    _conversations[session_id].append({"role": "assistant", "content": reply})

    logger.info(f"Session {session_id}: {len(_conversations[session_id])} messages")
    return reply


def clear_session(session_id: str) -> bool:
    """Delete the conversation history for ``session_id``.

    Returns ``True`` if the session existed and was removed, ``False`` otherwise.
    """
    if session_id not in _conversations:
        return False
    del _conversations[session_id]
    return True

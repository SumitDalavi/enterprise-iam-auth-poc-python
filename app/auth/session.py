"""Server-side session store backed by Redis."""
from __future__ import annotations
import json, os, secrets, time
from typing import Any, Optional

try:
    import redis
    _REDIS = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)
    _OK = True
except Exception:
    _OK = False
    _REDIS = None

SESSION_TTL = int(os.getenv("SESSION_TTL_SECONDS", "3600"))  # 1h default
_MEMORY_STORE: dict = {}  # fallback for dev without Redis


def create_session(user_id: str, data: dict = {}) -> str:
    """Create a new session and return the session token."""
    token = secrets.token_urlsafe(32)
    payload = json.dumps({"user_id": user_id, "created_at": time.time(), **data})
    if _OK and _REDIS:
        _REDIS.setex(f"session:{token}", SESSION_TTL, payload)
    else:
        _MEMORY_STORE[token] = payload
    return token


def get_session(token: str) -> Optional[dict]:
    """Retrieve session data. Returns None if expired or not found."""
    if _OK and _REDIS:
        raw = _REDIS.get(f"session:{token}")
    else:
        raw = _MEMORY_STORE.get(token)
    return json.loads(raw) if raw else None


def delete_session(token: str):
    """Invalidate (logout) a session."""
    if _OK and _REDIS:
        _REDIS.delete(f"session:{token}")
    else:
        _MEMORY_STORE.pop(token, None)


def refresh_session(token: str) -> bool:
    """Extend session TTL. Returns True if session existed."""
    if _OK and _REDIS:
        return bool(_REDIS.expire(f"session:{token}", SESSION_TTL))
    elif token in _MEMORY_STORE:
        return True
    return False

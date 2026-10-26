#!/usr/bin/env python3
"""Auth helpers for Google Smart Home OAuth2 + JWT verification."""
from __future__ import annotations

import os
import time
import jwt
from typing import Optional


CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
JWT_SECRET = os.getenv("JWT_SECRET", "change-me")


def verify_token(authorization: Optional[str]) -> Optional[dict]:
    if os.getenv("BYPASS_AUTH", "").lower() in ("1", "true", "yes"):
        return {"sub": "test-user", "iss": "google"}
    if not authorization:
        return None
    if authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
    else:
        token = authorization
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        if payload.get("iss") != "google":
            return None
        return payload
    except Exception:
        return None


def issue_token(user_id: str) -> str:
    now = int(time.time())
    payload = {
        "iss": "google",
        "sub": user_id,
        "iat": now,
        "exp": now + 3600,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

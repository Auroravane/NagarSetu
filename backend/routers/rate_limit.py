"""
Simple in-memory sliding window rate limiter for FastAPI endpoints.
Protects sensitive and resource-heavy routes (e.g. /api/chat) from abuse.
"""

from collections import defaultdict
import time
from typing import Dict, List, Tuple
from fastapi import HTTPException, Request, status


class SlidingWindowRateLimiter:
    """
    In-memory rate limiter tracking timestamps per client key.
    Note: In multi-worker deployments with separate process memory,
    rate limits are local per worker process.
    """

    def __init__(self, requests_limit: int = 30, window_seconds: int = 60):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        self._history: Dict[str, List[float]] = defaultdict(list)

    def _get_key(self, request: Request) -> str:
        # Prefer forwarded client IP if behind proxy, fallback to client host
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
        elif request.client:
            ip = request.client.host
        else:
            ip = "unknown"
        return ip

    def check(self, request: Request) -> None:
        key = self._get_key(request)
        now = time.time()
        window_start = now - self.window_seconds

        # Prune older entries
        timestamps = [ts for ts in self._history[key] if ts > window_start]
        if len(timestamps) >= self.requests_limit:
            self._history[key] = timestamps
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please slow down and try again shortly.",
            )

        timestamps.append(now)
        self._history[key] = timestamps

    def reset(self) -> None:
        self._history.clear()


chat_limiter = SlidingWindowRateLimiter(requests_limit=30, window_seconds=60)

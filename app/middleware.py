from __future__ import annotations

import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # A worker can process multiple requests in sequence.  Start with an
        # empty context so values from a previous request never leak into logs.
        clear_contextvars()

        # Preserve a caller-supplied request ID to support cross-service
        # correlation.  Requests without one receive a compact, traceable ID.
        correlation_id = request.headers.get("x-request-id") or f"req-{uuid.uuid4().hex[:8]}"
        bind_contextvars(correlation_id=correlation_id)
        request.state.correlation_id = correlation_id

        start = time.perf_counter()
        try:
            response = await call_next(request)
            response.headers["x-request-id"] = correlation_id
            response.headers["x-response-time-ms"] = str(
                int((time.perf_counter() - start) * 1000)
            )
            return response
        finally:
            # Reset after the response is prepared as well, which is important
            # for sequential requests handled by the same worker.
            clear_contextvars()

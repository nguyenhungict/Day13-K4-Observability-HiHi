from __future__ import annotations

import os
from typing import Any

try:
    from langfuse import Langfuse, observe

    LANGFUSE_SDK_AVAILABLE = True
except ImportError:  # pragma: no cover - chỉ dùng khi chưa cài requirements
    LANGFUSE_SDK_AVAILABLE = False

    def observe(*args: Any, **kwargs: Any):
        def decorator(func):
            return func

        return decorator

    class _DummyClient:
        def update_current_trace(self, **kwargs: Any) -> None:
            return None

        def update_current_generation(self, **kwargs: Any) -> None:
            return None

    def get_client():
        return _DummyClient()


def get_langfuse_client():
    # Cloud v4 ingests older Python SDK telemetry asynchronously unless this
    # OTLP header is present. Langfuse v3 supports additional exporter headers,
    # so retain the lab's pinned SDK while requesting real-time ingestion.
    if LANGFUSE_SDK_AVAILABLE:
        return Langfuse(
            additional_headers={"x-langfuse-ingestion-version": "4"}
        )
    return get_client()


def tracing_enabled() -> bool:
    return LANGFUSE_SDK_AVAILABLE and bool(
        os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY")
    )

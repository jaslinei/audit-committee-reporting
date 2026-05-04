"""
Day 9 — AI Developer 2
meta_builder.py — builds the meta object added to every AI endpoint response.

Usage in any route:
    from services.meta_builder import build_meta
    import time

    t_start = time.time()
    # ... do AI call ...
    meta = build_meta(t_start, cached=False)

Meta object returned:
    {
        "confidence":       0.0-1.0,
        "model_used":       "llama-3.3-70b-versatile",
        "tokens_used":      123,
        "response_time_ms": 456,
        "cached":           false
    }
"""

import time
import logging
from services.groq_client import groq_client

logger = logging.getLogger(__name__)


def build_meta(
    t_start: float,
    cached: bool,
    confidence: float = 1.0,
    tokens_used: int = 0,
) -> dict:
    """
    Build the standard meta object for every AI response.

    Args:
        t_start:     time.time() value recorded before the AI call.
        cached:      True if result came from Redis cache.
        confidence:  Confidence score 0.0-1.0 (default 1.0).
        tokens_used: Number of tokens used in the Groq call (default 0).

    Returns:
        dict with confidence, model_used, tokens_used,
        response_time_ms, cached.
    """
    return {
        "confidence":       round(max(0.0, min(1.0, confidence)), 2),
        "model_used":       groq_client.model_name,
        "tokens_used":      tokens_used,
        "response_time_ms": round((time.time() - t_start) * 1000),
        "cached":           cached,
    }


def build_fallback_meta(t_start: float) -> dict:
    """
    Build meta object for fallback responses (when Groq is unavailable).
    """
    return {
        "confidence":       0.0,
        "model_used":       groq_client.model_name,
        "tokens_used":      0,
        "response_time_ms": round((time.time() - t_start) * 1000),
        "cached":           False,
        "is_fallback":      True,
    }
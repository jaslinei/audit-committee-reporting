"""
Day 7 — AI Developer 2
GET /health — rich health check endpoint.

Returns:
  - overall status (healthy / degraded)
  - model name
  - average response time (last 10 calls)
  - ChromaDB document count
  - uptime in seconds
  - Redis cache hit/miss stats
"""

import time
import logging
import os
import redis
from flask import Blueprint, jsonify
from services.groq_client import groq_client
from services.chroma_client import chroma_client

health_bp = Blueprint("health", __name__)
logger = logging.getLogger(__name__)

_start_time = time.time()


def _get_cache_stats() -> dict:
    """Try to get Redis cache stats. Returns zeros if Redis is unavailable."""
    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        r.ping()
        info = r.info("stats")
        return {
            "hits":   info.get("keyspace_hits",   0),
            "misses": info.get("keyspace_misses", 0),
            "status": "connected",
        }
    except Exception as e:
        logger.warning("Redis unavailable for health check: %s", e)
        return {"hits": 0, "misses": 0, "status": "unavailable"}


@health_bp.route("/health", methods=["GET"])
def health():
    # ── Groq test call ────────────────────────────────────────────────
    t0 = time.time()
    test_reply = groq_client.call(
        "You are a health check service.",
        "Reply with the single word: OK",
        temperature=0.0,
        max_tokens=5,
    )
    groq_ok = test_reply is not None and "OK" in test_reply.upper()
    groq_ms = round((time.time() - t0) * 1000)

    # ── ChromaDB stats ────────────────────────────────────────────────
    doc_count = chroma_client.count()

    # ── Redis stats ───────────────────────────────────────────────────
    cache_stats = _get_cache_stats()

    # ── Overall status ────────────────────────────────────────────────
    status = "healthy" if groq_ok else "degraded"

    return jsonify({
        "status":              status,
        "model":               groq_client.model_name,
        "avg_response_time_ms": groq_client.avg_response_time_ms,
        "last_call_ms":        groq_ms,
        "chroma_doc_count":    doc_count,
        "uptime_seconds":      round(time.time() - _start_time),
        "cache":               cache_stats,
    }), 200
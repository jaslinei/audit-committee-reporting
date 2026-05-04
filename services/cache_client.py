"""
Day 8 — AI Developer 2
Redis AI response cache.

Features:
  - SHA256 cache key from prompt + input (same input = same key)
  - 15 minute TTL (900 seconds)
  - hit/miss counters tracked in Redis
  - Graceful fallback — if Redis is down, cache is skipped silently
  - Single singleton instance imported by all routes

Usage in any route:
    from services.cache_client import cache_client

    # Check cache first
    cached = cache_client.get(SYSTEM_PROMPT, text)
    if cached:
        return jsonify({**cached, "cached": True}), 200

    # Call Groq
    result = groq_client.call(SYSTEM_PROMPT, text)

    # Store in cache
    cache_client.set(SYSTEM_PROMPT, text, {"output": result})
"""

import os
import json
import hashlib
import logging
import redis
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

TTL_SECONDS = 900  # 15 minutes


class CacheClient:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        try:
            self.r = redis.from_url(redis_url, decode_responses=True)
            self.r.ping()
            self._available = True
            logger.info("CacheClient: Redis connected at %s", redis_url)
        except Exception as e:
            self._available = False
            logger.warning(
                "CacheClient: Redis unavailable (%s) — caching disabled", e
            )

    # ------------------------------------------------------------------
    # Key generation
    # ------------------------------------------------------------------

    def _key(self, system_prompt: str, input_text: str) -> str:
        """Generate a deterministic SHA256 cache key."""
        raw = f"{system_prompt}||{input_text}"
        return "ai_cache:" + hashlib.sha256(raw.encode()).hexdigest()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get(self, system_prompt: str, input_text: str) -> dict | None:
        """
        Look up a cached result.

        Returns:
            Parsed dict if cache hit, None if miss or Redis unavailable.
        """
        if not self._available:
            return None
        try:
            val = self.r.get(self._key(system_prompt, input_text))
            if val:
                self.r.incr("ai_cache:hits")
                logger.info("CacheClient: cache HIT")
                return json.loads(val)
            self.r.incr("ai_cache:misses")
            logger.info("CacheClient: cache MISS")
            return None
        except Exception as e:
            logger.warning("CacheClient get error: %s", e)
            return None

    def set(self, system_prompt: str, input_text: str, result: dict) -> bool:
        """
        Store a result in cache with 15-minute TTL.

        Returns:
            True on success, False on failure.
        """
        if not self._available:
            return False
        try:
            key = self._key(system_prompt, input_text)
            self.r.setex(key, TTL_SECONDS, json.dumps(result))
            logger.info("CacheClient: stored key with TTL=%ds", TTL_SECONDS)
            return True
        except Exception as e:
            logger.warning("CacheClient set error: %s", e)
            return False

    def get_stats(self) -> dict:
        """Return hit/miss counters for the /health endpoint."""
        if not self._available:
            return {"hits": 0, "misses": 0, "status": "unavailable"}
        try:
            hits   = int(self.r.get("ai_cache:hits")   or 0)
            misses = int(self.r.get("ai_cache:misses") or 0)
            return {"hits": hits, "misses": misses, "status": "connected"}
        except Exception as e:
            logger.warning("CacheClient stats error: %s", e)
            return {"hits": 0, "misses": 0, "status": "error"}

    @property
    def available(self) -> bool:
        return self._available


# ---------------------------------------------------------------------------
# Singleton — import this everywhere:
#   from services.cache_client import cache_client
# ---------------------------------------------------------------------------
cache_client = CacheClient()
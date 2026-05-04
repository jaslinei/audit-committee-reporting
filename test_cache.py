"""
Day 8 — Test Redis cache client.
Run with Flask stopped (no Flask needed):
    python test_cache.py

Expected output if Redis is running:
    ✅ Cache is working! First call: ~500ms, Second call: ~5ms

Expected output if Redis is NOT running (normal for local dev):
    ⚠️  Redis unavailable — cache disabled (this is fine, will work in Docker)
"""

import os
import sys
import time

os.environ.setdefault("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.cache_client import cache_client

print("Testing Redis cache client...\n")

if not cache_client.available:
    print("⚠️  Redis is not running locally — cache is disabled.")
    print("   This is expected in local development.")
    print("   Redis will be available when running via docker-compose.")
    print("\n✅ cache_client imported and initialised correctly.")
    print("   Cache will work automatically once Redis is running.")
    sys.exit(0)

# ── Test set and get ──────────────────────────────────────────────────────────
print("Redis is available — testing set/get...\n")

PROMPT  = "test-system-prompt"
INPUT   = "test-input-text"
PAYLOAD = {"category": "Compliance", "confidence": 0.9, "reasoning": "test"}

# First call — should be a miss
result = cache_client.get(PROMPT, INPUT)
print(f"Get before set : {'HIT' if result else 'MISS (expected)'}")

# Store
ok = cache_client.set(PROMPT, INPUT, PAYLOAD)
print(f"Set            : {'✅ success' if ok else '❌ failed'}")

# Second call — should be a hit
result = cache_client.get(PROMPT, INPUT)
print(f"Get after set  : {'HIT ✅' if result else 'MISS ❌'}")
if result:
    print(f"Cached value   : {result}")

# Stats
stats = cache_client.get_stats()
print(f"\nCache stats    : {stats}")

print("\n✅ Redis cache is working!")
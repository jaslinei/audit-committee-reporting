"""
Day 4 — Test ChromaDB setup.
Run this ONCE to confirm ChromaDB + sentence-transformers are working.

Run (Flask does NOT need to be running for this test):
    python test_chroma.py

Expected output:
    ✅ ChromaDB is working!
    Docs stored : 3
    Query result: <most relevant sentence>
    Distance    : <number close to 0 = very similar>
"""

import sys
import os

os.environ.setdefault("GROQ_API_KEY", "test")  # avoid GroqClient error on import

from services.chroma_client import chroma_client

print("Testing ChromaDB + sentence-transformers...\n")

# ── Step 1: add 3 test documents ──────────────────────────────────────────
docs = [
    ("doc-test-1", "Audit committees are responsible for overseeing financial reporting.", {"topic": "governance"}),
    ("doc-test-2", "Internal controls prevent fraud and ensure accurate financial statements.", {"topic": "controls"}),
    ("doc-test-3", "Cybersecurity risks must be regularly assessed and reported to the board.", {"topic": "IT"}),
]

print("Adding 3 test documents...")
for doc_id, text, meta in docs:
    ok = chroma_client.add(doc_id, text, meta)
    print(f"  {'✅' if ok else '❌'} {doc_id} — {text[:50]}...")

# ── Step 2: verify count ──────────────────────────────────────────────────
count = chroma_client.count()
print(f"\nDocs stored: {count}")
assert count >= 3, f"Expected at least 3 docs, got {count}"

# ── Step 3: query ─────────────────────────────────────────────────────────
print("\nQuerying: 'financial oversight and fraud prevention'")
results = chroma_client.query("financial oversight and fraud prevention", n_results=2)

if not results:
    print("❌ Query returned no results")
    sys.exit(1)

for i, r in enumerate(results, 1):
    print(f"\n  Result {i}:")
    print(f"    Text    : {r['text']}")
    print(f"    Metadata: {r['metadata']}")
    print(f"    Distance: {r['distance']}  (lower = more similar)")

# ── Step 4: cleanup test docs ─────────────────────────────────────────────
print("\nCleaning up test documents...")
for doc_id, _, _ in docs:
    chroma_client.delete(doc_id)
print(f"  Docs after cleanup: {chroma_client.count()}")

print("\n✅ ChromaDB is working!")
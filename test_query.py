"""
Day 5 — Test POST /query RAG endpoint.
Run AFTER seeding ChromaDB and starting Flask.

Steps:
    1. python seed_chroma.py       (seeds knowledge base)
    2. python app.py               (start Flask in terminal 1)
    3. python test_query.py        (run this in terminal 2)
"""

import requests

BASE = "http://localhost:5000"

questions = [
    "What is the role of the audit committee?",
    "How can organisations prevent fraud?",
    "What are IT general controls?",
    "What does GDPR say about data retention?",
    "Why is segregation of duties important?",
]

print("Testing POST /query (RAG)\n" + "="*50)

for i, question in enumerate(questions, 1):
    resp = requests.post(f"{BASE}/query", json={"question": question})
    data = resp.json()

    print(f"\nTest {i}: {question}")
    print(f"  Answer   : {data.get('answer', '')[:120]}...")
    print(f"  Sources  : {len(data.get('sources', []))} chunks retrieved")
    print(f"  Fallback : {data.get('is_fallback')}")
    print(f"  Time (ms): {data.get('meta', {}).get('response_time_ms')}")
    print(f"  Chunks   : {data.get('meta', {}).get('chunks_retrieved')}")
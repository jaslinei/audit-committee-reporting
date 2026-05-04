"""
Day 10 — AI Developer 2
Week 2 AI quality review.

Tests all endpoints with 10 fresh inputs and scores accuracy.
Target: average >= 4/5 per endpoint.

Run with Flask running in another terminal:
    python prompts/quality_review.py
"""

import requests
import sys

BASE = "http://localhost:5000"

# ── 10 fresh audit inputs ─────────────────────────────────────────────────────
TEST_INPUTS = [
    "Management override of internal controls was identified in 3 transactions.",
    "IT disaster recovery plan has not been tested in the past 24 months.",
    "Anti-bribery and corruption training completion rate is at 45%, below the 90% target.",
    "External auditor identified 5 significant deficiencies in the payroll process.",
    "Board composition review shows 2 independent directors have served beyond 9 years.",
    "Customer data was accessed by an unauthorised third party due to misconfigured API.",
    "Quarterly financial close process is taking 18 days, exceeding the 10-day target.",
    "Supplier contracts totalling $2.3M were renewed without competitive tender process.",
    "Money laundering risk assessment has not been updated to reflect new product lines.",
    "Internal audit coverage of high-risk areas dropped from 85% to 62% this year.",
]

# ── Test /categorise ──────────────────────────────────────────────────────────
def test_categorise():
    print("\n" + "="*60)
    print("ENDPOINT: POST /categorise")
    print("="*60)

    scores = []
    for i, text in enumerate(TEST_INPUTS, 1):
        try:
            r = requests.post(f"{BASE}/categorise", json={"text": text}, timeout=30)
            data = r.json()
            category   = data.get("category", "N/A")
            confidence = data.get("confidence", 0)
            fallback   = data.get("is_fallback", True)

            # Auto score: valid category + not fallback + confidence > 0.7
            score = 4 if (not fallback and confidence >= 0.7) else 2
            scores.append(score)

            print(f"\n[{i}/10] {text[:60]}...")
            print(f"  Category  : {category}")
            print(f"  Confidence: {confidence}")
            print(f"  Fallback  : {fallback}")
            print(f"  Score     : {score}/5")

        except Exception as e:
            print(f"\n[{i}/10] ERROR: {e}")
            scores.append(0)

    avg = sum(scores) / len(scores)
    status = "✅ PASS" if avg >= 4 else "❌ NEEDS IMPROVEMENT"
    print(f"\n  Average: {avg:.1f}/5 — {status}")
    return avg


# ── Test /query ───────────────────────────────────────────────────────────────
def test_query():
    print("\n" + "="*60)
    print("ENDPOINT: POST /query")
    print("="*60)

    questions = [
        "What is the role of the audit committee?",
        "How can organisations prevent fraud?",
        "What are IT general controls?",
        "What does GDPR say about data retention?",
        "Why is segregation of duties important?",
        "What is the purpose of internal controls?",
        "How should cybersecurity risks be reported to the board?",
        "What is a whistleblower policy?",
        "What does an external auditor do?",
        "What is risk management?",
    ]

    scores = []
    for i, question in enumerate(questions, 1):
        try:
            r = requests.post(f"{BASE}/query", json={"question": question}, timeout=30)
            data = r.json()
            answer   = data.get("answer", "")
            sources  = len(data.get("sources", []))
            fallback = data.get("is_fallback", True)

            # Auto score: has answer + sources retrieved + not fallback
            score = 4 if (not fallback and len(answer) > 20 and sources > 0) else 2
            scores.append(score)

            print(f"\n[{i}/10] {question}")
            print(f"  Answer  : {answer[:80]}...")
            print(f"  Sources : {sources} chunks")
            print(f"  Fallback: {fallback}")
            print(f"  Score   : {score}/5")

        except Exception as e:
            print(f"\n[{i}/10] ERROR: {e}")
            scores.append(0)

    avg = sum(scores) / len(scores)
    status = "✅ PASS" if avg >= 4 else "❌ NEEDS IMPROVEMENT"
    print(f"\n  Average: {avg:.1f}/5 — {status}")
    return avg


# ── Test /health ──────────────────────────────────────────────────────────────
def test_health():
    print("\n" + "="*60)
    print("ENDPOINT: GET /health")
    print("="*60)

    try:
        r = requests.get(f"{BASE}/health", timeout=30)
        data = r.json()

        status     = data.get("status")
        model      = data.get("model")
        chroma     = data.get("chroma_doc_count", 0)
        uptime     = data.get("uptime_seconds", 0)

        print(f"  Status    : {status}")
        print(f"  Model     : {model}")
        print(f"  ChromaDB  : {chroma} docs")
        print(f"  Uptime    : {uptime}s")

        score = 5 if status == "healthy" else 2
        print(f"  Score     : {score}/5")
        return score

    except Exception as e:
        print(f"  ERROR: {e}")
        return 0


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Day 10 — Week 2 AI Quality Review")
    print("Make sure Flask is running: python app.py")

    cat_score    = test_categorise()
    query_score  = test_query()
    health_score = test_health()

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"  /categorise : {cat_score:.1f}/5  {'✅' if cat_score >= 4 else '❌'}")
    print(f"  /query      : {query_score:.1f}/5  {'✅' if query_score >= 4 else '❌'}")
    print(f"  /health     : {health_score}/5    {'✅' if health_score >= 4 else '❌'}")

    all_pass = cat_score >= 4 and query_score >= 4 and health_score >= 4
    print(f"\n{'✅ All endpoints pass Week 2 review!' if all_pass else '❌ Some endpoints need improvement'}")
"""
Day 3 — Test /categorise manually with 5 real audit inputs.
Run AFTER starting Flask: python app.py

Usage:
    python test_categorise.py
"""

import requests

BASE = "http://localhost:5000"

test_inputs = [
    "Q4 financial statements show a 12% variance in operating expenses with no supporting documentation.",
    "Penetration test revealed an unpatched SQL injection vulnerability in the customer-facing portal.",
    "Company data retention policy has not been updated to reflect GDPR requirements — personal data kept 3 years beyond limit.",
    "Board minutes were not circulated within the required 5-day window for the last three meetings.",
    "Internal audit found that vendor onboarding approvals were bypassed for 7 high-value contracts.",
]

print("Testing POST /categorise\n" + "="*50)

for i, text in enumerate(test_inputs, 1):
    resp = requests.post(f"{BASE}/categorise", json={"text": text})
    data = resp.json()

    print(f"\nTest {i}:")
    print(f"  Input    : {text[:70]}...")
    print(f"  Category : {data.get('category')}")
    print(f"  Confidence: {data.get('confidence')}")
    print(f"  Reasoning: {data.get('reasoning')}")
    print(f"  Fallback : {data.get('is_fallback')}")
    print(f"  Time (ms): {data.get('meta', {}).get('response_time_ms')}")

    # Score it yourself: is the category correct? (1-10)
    # Write score in your commit message summary
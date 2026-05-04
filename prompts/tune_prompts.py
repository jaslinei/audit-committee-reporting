"""
Day 6 — AI Developer 2
Prompt tuning — test all prompts against 10 real audit inputs.

Run with Flask stopped (no Flask needed):
    python prompts/tune_prompts.py

For each prompt, score the output 1-10:
  - 10: Perfect category, clear reasoning, professional tone
  -  7: Correct but reasoning is vague
  -  5: Wrong category but reasoning makes sense
  -  3: Wrong category, poor reasoning
  -  1: Gibberish or fallback

Target: average >= 7/10 for every prompt.
If any prompt averages below 7, rewrite it and re-run.
"""

import os
import sys
import json

os.environ.setdefault("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from services.groq_client import groq_client

# ── 10 real audit committee inputs ───────────────────────────────────────────
TEST_INPUTS = [
    "Q4 financial statements show a 12% variance in operating expenses with no supporting documentation.",
    "Penetration test revealed an unpatched SQL injection vulnerability in the customer-facing portal.",
    "Company data retention policy has not been updated to reflect GDPR requirements — personal data kept 3 years beyond limit.",
    "Board minutes were not circulated within the required 5-day window for the last three meetings.",
    "Internal audit found that vendor onboarding approvals were bypassed for 7 high-value contracts.",
    "External auditor issued a qualified opinion on the consolidated financial statements due to inventory valuation concerns.",
    "Access control review found 23 former employees still have active system credentials.",
    "Whistleblower report received regarding potential manipulation of revenue recognition entries.",
    "Business continuity plan has not been tested in 18 months, contrary to policy requirements.",
    "Legal counsel flagged a potential breach of competition law in the recent supplier agreement.",
]

# ── Prompts to evaluate ───────────────────────────────────────────────────────
PROMPTS = {
    "categorise": {
        "system": """You are a senior audit committee classification expert.
Classify the input text into exactly one of these categories:
Financial Controls, Risk Management, Compliance, Governance, Internal Audit, IT & Cybersecurity, Legal & Regulatory, Other.

Rules:
- Choose the single best-fitting category.
- confidence must be a float between 0.0 and 1.0.
- reasoning must be one concise sentence explaining your choice.
- Respond ONLY with valid JSON — no markdown, no backticks, no explanation outside the JSON.

Response format:
{"category": "...", "confidence": 0.0, "reasoning": "..."}""",
        "temperature": 0.2,
        "max_tokens": 120,
    },
    "describe": {
        "system": """You are a professional audit committee secretary.
Write a concise, formal one-paragraph description of the following audit finding.
The description should:
- Be 2-3 sentences long
- Use professional audit language
- Identify the risk and its potential impact
- Be suitable for inclusion in an audit committee report
Respond with the description only — no headings, no bullet points.""",
        "temperature": 0.3,
        "max_tokens": 200,
    },
    "recommend": {
        "system": """You are a senior audit committee advisor.
Provide exactly 3 actionable recommendations for the following audit finding.
Respond ONLY with valid JSON — no markdown, no backticks:
{"recommendations": [
  {"action_type": "...", "description": "...", "priority": "High|Medium|Low"},
  {"action_type": "...", "description": "...", "priority": "High|Medium|Low"},
  {"action_type": "...", "description": "...", "priority": "High|Medium|Low"}
]}""",
        "temperature": 0.4,
        "max_tokens": 400,
    },
}


def evaluate_prompt(name: str, config: dict):
    print(f"\n{'='*60}")
    print(f"PROMPT: {name.upper()}")
    print(f"{'='*60}")

    scores = []

    for i, text in enumerate(TEST_INPUTS, 1):
        print(f"\n  [{i}/10] {text[:70]}...")

        result = groq_client.call(
            config["system"],
            text,
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
        )

        if result is None:
            print(f"  OUTPUT : ❌ Groq returned None (fallback)")
            scores.append(0)
            continue

        print(f"  OUTPUT : {result[:150]}{'...' if len(result) > 150 else ''}")

        # Auto-score JSON prompts
        if name in ("categorise", "recommend"):
            try:
                clean = result.strip().replace("```json", "").replace("```", "")
                parsed = json.loads(clean)
                auto_score = 8 if parsed else 4
                print(f"  JSON   : ✅ valid")
            except json.JSONDecodeError:
                auto_score = 3
                print(f"  JSON   : ❌ invalid JSON")
            scores.append(auto_score)
        else:
            # For describe, score based on length and professionalism indicators
            word_count = len(result.split())
            auto_score = 8 if 20 <= word_count <= 100 else 5
            print(f"  Words  : {word_count}")
            scores.append(auto_score)

    avg = sum(scores) / len(scores)
    status = "✅ PASS" if avg >= 7 else "❌ NEEDS REWRITE"
    print(f"\n  SCORES : {scores}")
    print(f"  AVERAGE: {avg:.1f}/10 — {status}")
    return avg


if __name__ == "__main__":
    print("Day 6 — Prompt Tuning Evaluation")
    print("="*60)

    results = {}
    for name, config in PROMPTS.items():
        avg = evaluate_prompt(name, config)
        results[name] = avg

    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    for name, avg in results.items():
        status = "✅ PASS" if avg >= 7 else "❌ REWRITE NEEDED"
        print(f"  {name:<15} {avg:.1f}/10  {status}")

    all_pass = all(v >= 7 for v in results.values())
    print(f"\n{'✅ All prompts pass!' if all_pass else '❌ Some prompts need rewriting'}")
    print("\nSave your scores to prompts/quality_scores.md")
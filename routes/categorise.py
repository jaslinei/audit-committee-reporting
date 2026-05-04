"""
Day 3 — AI Developer 2
POST /categorise

Classifies an audit committee item into a predefined category.
Returns: { category, confidence, reasoning, meta, is_fallback }
"""

import json
import time
import logging
from flask import Blueprint, request, jsonify
from services.groq_client import groq_client

categorise_bp = Blueprint("categorise", __name__)
logger = logging.getLogger(__name__)

CATEGORIES = [
    "Financial Controls",
    "Risk Management",
    "Compliance",
    "Governance",
    "Internal Audit",
    "IT & Cybersecurity",
    "Legal & Regulatory",
    "Other",
]

SYSTEM_PROMPT = f"""You are a senior audit committee classification expert.
Classify the input text into exactly one of these categories:
{", ".join(CATEGORIES)}

Rules:
- Choose the single best-fitting category.
- confidence must be a float between 0.0 and 1.0.
- reasoning must be one concise sentence explaining your choice.
- Respond ONLY with valid JSON — no markdown, no backticks, no explanation outside the JSON.

Response format:
{{"category": "...", "confidence": 0.0, "reasoning": "..."}}"""

FALLBACK = {
    "category": "Other",
    "confidence": 0.0,
    "reasoning": "AI service unavailable — please retry.",
    "is_fallback": True,
}


@categorise_bp.route("/categorise", methods=["POST"])
def categorise():
    t_start = time.time()

    data = request.get_json(silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "text field is required"}), 400

    if len(text) > 5000:
        return jsonify({"error": "text must be 5000 characters or fewer"}), 400

    raw = groq_client.call(SYSTEM_PROMPT, text, temperature=0.2, max_tokens=120)

    if raw is None:
        logger.warning("categorise: groq_client returned None, using fallback")
        result = {**FALLBACK, "meta": _meta(t_start, cached=False)}
        return jsonify(result), 200

    try:
        clean = raw.strip().replace("```json", "").replace("```", "").strip()
        parsed = json.loads(clean)

        if parsed.get("category") not in CATEGORIES:
            parsed["category"] = "Other"

        parsed["confidence"] = round(float(parsed.get("confidence", 0.0)), 2)
        parsed["is_fallback"] = False
        parsed["meta"] = _meta(t_start, cached=False)

        return jsonify(parsed), 200

    except (json.JSONDecodeError, ValueError) as e:
        logger.error("categorise: JSON parse failed — raw=%s error=%s", raw, e)
        result = {**FALLBACK, "meta": _meta(t_start, cached=False)}
        return jsonify(result), 200


def _meta(t_start: float, cached: bool) -> dict:
    return {
        "model_used": groq_client.model_name,
        "response_time_ms": round((time.time() - t_start) * 1000),
        "cached": cached,
    }
"""
Day 5 — AI Developer 2
POST /query — RAG (Retrieval-Augmented Generation) endpoint.

Flow:
  1. Embed the question using sentence-transformers
  2. Retrieve top-3 most relevant chunks from ChromaDB
  3. Inject chunks as context into the Groq prompt
  4. Return answer + sources

Returns: { answer, sources, meta, is_fallback }
"""

import time
import logging
from flask import Blueprint, request, jsonify
from services.groq_client import groq_client
from services.chroma_client import chroma_client

query_bp = Blueprint("query", __name__)
logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert audit committee advisor.
Use ONLY the context provided below to answer the question.
Be concise, professional, and factual.
If the context does not contain enough information to answer, say:
"I don't have enough information in my knowledge base to answer that question."
Do not make up information that is not in the context."""

FALLBACK_ANSWER = (
    "AI service is temporarily unavailable. "
    "Please retry in a moment."
)


@query_bp.route("/query", methods=["POST"])
def rag_query():
    t_start = time.time()

    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "question field is required"}), 400

    if len(question) > 2000:
        return jsonify({"error": "question must be 2000 characters or fewer"}), 400

    # ── Step 1: retrieve relevant chunks from ChromaDB ────────────────
    chunks = chroma_client.query(question, n_results=3)

    if not chunks:
        logger.warning("query: ChromaDB returned no chunks — collection may be empty")
        context = "No relevant documents found in the knowledge base."
    else:
        context = "\n\n".join(
            f"[Source {i+1}]: {c['text']}"
            for i, c in enumerate(chunks)
        )

    # ── Step 2: call Groq with context + question ─────────────────────
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"
    answer = groq_client.call(
        SYSTEM_PROMPT,
        user_prompt,
        temperature=0.3,
        max_tokens=500,
    )

    # ── Step 3: build response ────────────────────────────────────────
    if answer is None:
        logger.warning("query: groq_client returned None, using fallback")
        return jsonify({
            "answer":      FALLBACK_ANSWER,
            "sources":     [],
            "is_fallback": True,
            "meta":        _meta(t_start, cached=False, chunks=0),
        }), 200

    sources = [
        {
            "text":     c["text"][:120] + "..." if len(c["text"]) > 120 else c["text"],
            "metadata": c["metadata"],
            "distance": c["distance"],
        }
        for c in chunks
    ]

    return jsonify({
        "answer":      answer,
        "sources":     sources,
        "is_fallback": False,
        "meta":        _meta(t_start, cached=False, chunks=len(chunks)),
    }), 200


def _meta(t_start: float, cached: bool, chunks: int) -> dict:
    return {
        "model_used":       groq_client.model_name,
        "response_time_ms": round((time.time() - t_start) * 1000),
        "cached":           cached,
        "chunks_retrieved": chunks,
    }
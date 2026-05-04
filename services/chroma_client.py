"""
Day 4 — AI Developer 2
ChromaDB client — vector database for the RAG pipeline.

Features:
  - Persistent storage in ./chroma_data (survives restarts)
  - Embeds text using sentence-transformers (all-MiniLM-L6-v2)
  - add()   — store a document with metadata
  - query() — find top-N most similar documents
  - count() — total docs stored (used by /health)
  - Single singleton instance imported by all routes
"""

import logging
import chromadb
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

COLLECTION_NAME = "audit_knowledge"
EMBED_MODEL     = "all-MiniLM-L6-v2"


class ChromaClient:
    def __init__(self):
        logger.info("ChromaDB: loading embedding model '%s' ...", EMBED_MODEL)
        self.model = SentenceTransformer(EMBED_MODEL)
        logger.info("ChromaDB: model loaded")

        self.client = chromadb.PersistentClient(path="./chroma_data")
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        logger.info(
            "ChromaDB: collection '%s' ready — %d docs",
            COLLECTION_NAME,
            self.collection.count(),
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def embed(self, text: str) -> list[float]:
        """Convert text to a vector embedding."""
        return self.model.encode(text).tolist()

    def add(self, doc_id: str, text: str, metadata: dict = {}) -> bool:
        """
        Store a document in ChromaDB.

        Args:
            doc_id:   Unique string ID (e.g. "doc-001").
            text:     The document text to embed and store.
            metadata: Optional dict of key-value pairs (source, topic, etc.)

        Returns:
            True on success, False on failure.
        """
        try:
            self.collection.add(
                ids=[doc_id],
                embeddings=[self.embed(text)],
                documents=[text],
                metadatas=[metadata],
            )
            logger.info("ChromaDB: added doc_id=%s", doc_id)
            return True
        except Exception as e:
            logger.error("ChromaDB add failed doc_id=%s error=%s", doc_id, e)
            return False

    def query(self, text: str, n_results: int = 3) -> list[dict]:
        """
        Find the most semantically similar documents.

        Args:
            text:      The query text to search for.
            n_results: Number of results to return (default 3).

        Returns:
            List of dicts with keys: text, metadata, distance
            Empty list if collection is empty or query fails.
        """
        try:
            total = self.collection.count()
            if total == 0:
                logger.warning("ChromaDB: collection is empty, returning []")
                return []

            # Can't return more results than docs stored
            n = min(n_results, total)

            results = self.collection.query(
                query_embeddings=[self.embed(text)],
                n_results=n,
            )

            docs      = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas",  [[]])[0]
            distances = results.get("distances",  [[]])[0]

            return [
                {
                    "text":     doc,
                    "metadata": meta,
                    "distance": round(dist, 4),
                }
                for doc, meta, dist in zip(docs, metadatas, distances)
            ]
        except Exception as e:
            logger.error("ChromaDB query failed: %s", e)
            return []

    def count(self) -> int:
        """Return total number of documents stored."""
        try:
            return self.collection.count()
        except Exception:
            return 0

    def delete(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        try:
            self.collection.delete(ids=[doc_id])
            return True
        except Exception as e:
            logger.error("ChromaDB delete failed doc_id=%s error=%s", doc_id, e)
            return False


# ---------------------------------------------------------------------------
# Singleton — import this everywhere:
#   from services.chroma_client import chroma_client
# ---------------------------------------------------------------------------
chroma_client = ChromaClient()
"""
Day 5 — Seed ChromaDB with audit committee knowledge documents.
These are used by the /query RAG endpoint to answer questions.

Run ONCE before testing /query:
    python seed_chroma.py

You can re-run safely — duplicate IDs are skipped.
"""

import os
os.environ.setdefault("GROQ_API_KEY", "test")

from services.chroma_client import chroma_client

DOCUMENTS = [
    (
        "audit-001",
        "The audit committee is responsible for overseeing the integrity of financial statements, "
        "the external audit process, and compliance with legal and regulatory requirements.",
        {"topic": "governance", "source": "audit-standards"},
    ),
    (
        "audit-002",
        "Internal controls are processes designed to provide reasonable assurance regarding the "
        "achievement of objectives in operations, financial reporting, and compliance.",
        {"topic": "internal-controls", "source": "coso-framework"},
    ),
    (
        "audit-003",
        "Risk management involves identifying, assessing, and prioritising risks followed by "
        "coordinated application of resources to minimise the probability of unfortunate events.",
        {"topic": "risk-management", "source": "iso-31000"},
    ),
    (
        "audit-004",
        "IT general controls include access controls, change management, and IT operations. "
        "Weak IT controls can undermine the reliability of financial reporting systems.",
        {"topic": "IT-controls", "source": "cobit"},
    ),
    (
        "audit-005",
        "Fraud risk factors include pressure, opportunity, and rationalisation. "
        "The audit committee should ensure management has anti-fraud programs in place.",
        {"topic": "fraud", "source": "isa-240"},
    ),
    (
        "audit-006",
        "GDPR requires organisations to retain personal data only for as long as necessary. "
        "Data retention policies must be documented and enforced across all systems.",
        {"topic": "compliance", "source": "gdpr"},
    ),
    (
        "audit-007",
        "External auditors provide an independent opinion on whether financial statements "
        "present a true and fair view in accordance with the applicable financial reporting framework.",
        {"topic": "external-audit", "source": "isa-700"},
    ),
    (
        "audit-008",
        "Segregation of duties is a key internal control that ensures no single individual "
        "has control over all aspects of a financial transaction, reducing fraud risk.",
        {"topic": "internal-controls", "source": "coso-framework"},
    ),
    (
        "audit-009",
        "Cybersecurity governance requires the board and audit committee to receive regular "
        "reports on cyber risks, incidents, and the effectiveness of security controls.",
        {"topic": "cybersecurity", "source": "nist"},
    ),
    (
        "audit-010",
        "Whistleblower policies enable employees to report concerns about financial irregularities "
        "or misconduct without fear of retaliation, supporting a strong control environment.",
        {"topic": "governance", "source": "sarbanes-oxley"},
    ),
]

print(f"Seeding ChromaDB with {len(DOCUMENTS)} audit knowledge documents...\n")

added = 0
skipped = 0

for doc_id, text, metadata in DOCUMENTS:
    ok = chroma_client.add(doc_id, text, metadata)
    if ok:
        print(f"  ✅ {doc_id} — {text[:60]}...")
        added += 1
    else:
        print(f"  ⚠️  {doc_id} — already exists or failed, skipping")
        skipped += 1

print(f"\nDone — added: {added}, skipped: {skipped}")
print(f"Total docs in ChromaDB: {chroma_client.count()}")
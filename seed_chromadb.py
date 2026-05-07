"""
seed_chromadb.py
Ingests 10 domain knowledge documents into ChromaDB for the Policy Lifecycle Manager RAG pipeline.
Run once to seed the database: python seed_chromadb.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# All 10 documents to ingest
DOCUMENTS = [
    "data/health_policy_1.txt",
    "data/life_policy_1.txt",
    "data/vehicle_policy_1.txt",
    "data/home_policy_1.txt",
    "data/travel_policy_1.txt",
    "data/business_policy_1.txt",
    "data/claims_process_1.txt",
    "data/policy_exclusions_1.txt",
    "data/policy_renewal_1.txt",
    "data/cyber_policy_1.txt",
]


def seed():
    print("=" * 50)
    print("Seeding ChromaDB with policy documents...")
    print("=" * 50)

    # Check all files exist before starting
    missing = [f for f in DOCUMENTS if not os.path.exists(f)]
    if missing:
        print(f"ERROR: Missing files: {missing}")
        sys.exit(1)

    print(f"Found all {len(DOCUMENTS)} documents. Loading...")

    # Import here to trigger sentence-transformers pre-load
    from services.rag_pipeline import rag_pipeline

    # Load all documents into ChromaDB
    rag_pipeline.load_documents_from_files(DOCUMENTS)

    print("\nDocuments ingested successfully!")
    print("=" * 50)

    # Verify by running a test query
    print("\nVerifying with test query...")
    test_question = "What does health insurance cover?"
    results = rag_pipeline.get_relevant_documents(test_question, k=3)

    if results:
        print(f"Verification passed! Found {len(results)} relevant documents.")
        print("\nSample result preview:")
        print(results[0][:200] + "...")
    else:
        print("WARNING: No results found. Check if documents loaded correctly.")

    print("\n" + "=" * 50)
    print("Seeding complete! ChromaDB is ready to use.")
    print("=" * 50)

    # Print summary
    print("\nDocuments loaded:")
    for i, doc in enumerate(DOCUMENTS, 1):
        print(f"  {i}. {doc}")


if __name__ == "__main__":
    seed()

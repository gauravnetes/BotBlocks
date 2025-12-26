"""
Test script to debug retrieval issues
"""

import os
import tempfile
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

# Your bot ID
BOT_ID = "4b26b240-d7ac-436b-a3b1-32727dadcd43"

print("=" * 70)
print("RETRIEVAL DEBUG TEST")
print("=" * 70)

# Initialize
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
collection_name = f"collection_{BOT_ID}"

print(f"\n1. Connecting to collection: {collection_name}")

vector_store = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings,
    collection_name=collection_name,
    collection_metadata={"hnsw:space": "cosine"}
)

doc_count = vector_store._collection.count()
print(f"   ✅ Collection has {doc_count} documents")

# Test query
query = "which dataset is used"
print(f"\n2. Testing query: '{query}'")

# Get top 5 results with scores
results = vector_store.similarity_search_with_relevance_scores(query, k=5)

print(f"\n3. Results ({len(results)} found):")
print("-" * 70)

for i, (doc, score) in enumerate(results, 1):
    print(f"\n📄 Result {i}:")
    print(f"   Score: {score:.4f}")
    print(f"   Content preview: {doc.page_content[:200]}...")
    print(f"   Source: {doc.metadata.get('source', 'N/A')}")

# Check metadata
print("\n4. Collection metadata:")
print(f"   {vector_store._collection.metadata}")

print("\n" + "=" * 70)
print("ANALYSIS:")
print("=" * 70)

if not results:
    print("❌ No results found!")
    print("   Possible issues:")
    print("   - Documents are in wrong collection")
    print("   - Embeddings mismatch")
    print("   - Query too different from document content")
elif results[0][1] < 0:
    print("❌ Negative scores detected!")
    print("   Collection is NOT using cosine similarity")
    print("   Run force_delete.py and re-upload")
elif results[0][1] < 0.3:
    print("⚠️  Low relevance scores (< 0.3)")
    print(f"   Best match: {results[0][1]:.4f}")
    print("   Query might be too generic or documents don't contain answer")
else:
    print("✅ Good scores! Should work with threshold 0.3")
    print(f"   Best match: {results[0][1]:.4f}")

print("=" * 70)
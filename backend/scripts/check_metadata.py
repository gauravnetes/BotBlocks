"""
Quick script to check if your collections are using cosine similarity
"""

import os
import tempfile
import chromadb

CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

print("=" * 70)
print("COLLECTION METADATA CHECKER")
print("=" * 70)

client = chromadb.PersistentClient(path=CHROMA_PATH)
collections = client.list_collections()

print(f"\nFound {len(collections)} collections:\n")

for col in collections:
    metadata = col.metadata if col.metadata else {}
    doc_count = col.count()
    
    distance_metric = metadata.get('hnsw:space', 'NOT SET (defaults to l2)') if metadata else 'NOT SET (defaults to l2)'
    
    print(f"📦 {col.name}")
    print(f"   Documents: {doc_count}")
    print(f"   Distance Metric: {distance_metric}")
    
    if distance_metric == 'cosine':
        print(f"   ✅ Using COSINE (CORRECT)")
    else:
        print(f"   ❌ Using L2 or unset (WRONG - causes negative scores)")
    
    print()

print("=" * 70)
print("SOLUTION:")
print("=" * 70)
print("If any collections show L2 or 'NOT SET', you need to:")
print("1. Delete that collection")
print("2. Re-upload the document")
print("3. Make sure your upload code has collection_metadata={'hnsw:space': 'cosine'}")
print("=" * 70)
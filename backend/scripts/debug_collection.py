"""
ChromaDB Collection Diagnostic Script
Run this to find where your documents actually are
"""

import os
import tempfile
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb

# Your current setup
CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

print("=" * 70)
print("CHROMADB DIAGNOSTIC TOOL")
print("=" * 70)

# Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Step 1: Check if ChromaDB path exists
print(f"\n1. Checking ChromaDB path: {CHROMA_PATH}")
if os.path.exists(CHROMA_PATH):
    print("   ✅ Path exists")
    print(f"   Files in directory: {os.listdir(CHROMA_PATH)}")
else:
    print("   ❌ Path does NOT exist!")
    print("   This means no data has been stored yet.")
    exit(1)

# Step 2: List ALL collections
print("\n2. Listing ALL collections in ChromaDB:")
try:
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collections = client.list_collections()
    
    if not collections:
        print("   ❌ No collections found at all!")
        print("   This means documents were never uploaded successfully.")
    else:
        print(f"   ✅ Found {len(collections)} collection(s):")
        for col in collections:
            count = col.count()
            print(f"      - '{col.name}': {count} documents")
            
            # Show sample metadata if documents exist
            if count > 0:
                sample = col.peek(limit=1)
                if sample and sample['metadatas']:
                    print(f"        Sample metadata: {sample['metadatas'][0]}")
    
except Exception as e:
    print(f"   ❌ Error listing collections: {e}")
    exit(1)

# Step 3: Check specific collection (collection_11)
print("\n3. Checking 'collection_11' specifically:")
try:
    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings,
        collection_name="collection_11",
        collection_metadata={"hnsw:space": "cosine"}
    )
    
    doc_count = vector_store._collection.count()
    print(f"   Document count: {doc_count}")
    
    if doc_count == 0:
        print("   ❌ Collection exists but has 0 documents")
        print("   This confirms the ID mismatch issue!")
    else:
        print(f"   ✅ Collection has {doc_count} documents")
        
except Exception as e:
    print(f"   ❌ Error accessing collection_11: {e}")

# Step 4: Recommendations
print("\n" + "=" * 70)
print("DIAGNOSIS SUMMARY")
print("=" * 70)

if collections:
    print("\n📋 Your collections:")
    for col in collections:
        print(f"   - {col.name}: {col.count()} documents")
    
    print("\n🔍 PROBLEM IDENTIFIED:")
    print("   Your documents exist, but under a DIFFERENT collection name!")
    print("\n💡 SOLUTION:")
    print("   1. Check your upload code - what collection_name does it use?")
    print("   2. Likely using bot.public_id instead of bot.id")
    print("   3. Fix: Use bot.id consistently in both upload and query")
else:
    print("\n❌ NO COLLECTIONS FOUND")
    print("\n💡 POSSIBLE CAUSES:")
    print("   1. Upload failed silently")
    print("   2. Wrong CHROMA_PATH used during upload")
    print("   3. Documents not committed/persisted")

print("\n" + "=" * 70)

# Step 5: Interactive fix helper
print("\n🛠️  QUICK FIX HELPER")
print("=" * 70)

if collections and len(collections) > 0:
    print("\nOption 1: Rename existing collection to 'collection_11'")
    print("   (Only if you know the correct collection)")
    print("\nOption 2: Re-upload documents using correct bot.id")
    print("   (Recommended)")
    
    # Show the code needed
    print("\n📝 Code to fix in your upload function:")
    print("""
# ❌ WRONG - If you're doing this:
collection_name = f"collection_{bot.public_id}"
# or
collection_name = f"collection_{bot.name}"

# ✅ CORRECT - Change to:
collection_name = f"collection_{bot.id}"  # Use database ID!
    """)
else:
    print("\nYou need to check your upload endpoint:")
    print("   1. Is it being called at all?")
    print("   2. Are there any errors in the logs?")
    print("   3. Is the ChromaDB path correct?")

print("\n" + "=" * 70)
print("Next steps: Run this script and share the output!")
print("=" * 70)
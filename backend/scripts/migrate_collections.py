"""
Migration script to convert existing collections to use cosine similarity.
This preserves your existing documents without needing to re-upload.
"""

import os
import tempfile
import chromadb
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from tqdm import tqdm

CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

def migrate_collection_to_cosine(collection_name: str, embeddings):
    """Migrate a single collection from L2 to cosine similarity"""
    
    print(f"\n📦 Migrating: {collection_name}")
    
    try:
        # Step 1: Connect to old collection (L2)
        old_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name
            # No metadata = defaults to L2
        )
        
        doc_count = old_store._collection.count()
        print(f"   Found {doc_count} documents")
        
        if doc_count == 0:
            print(f"   ⚠️  Empty collection, skipping...")
            return True
        
        # Step 2: Get all documents
        print(f"   📥 Retrieving all documents...")
        all_data = old_store._collection.get()
        
        documents = all_data['documents']
        metadatas = all_data['metadatas']
        ids = all_data['ids']
        
        print(f"   ✅ Retrieved {len(documents)} documents")
        
        # Step 3: Delete old collection
        print(f"   🗑️  Deleting old collection...")
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        client.delete_collection(collection_name)
        
        # Step 4: Create new collection with cosine
        print(f"   🔨 Creating new collection with cosine similarity...")
        new_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"}  # ← KEY FIX
        )
        
        # Step 5: Re-add all documents
        print(f"   📤 Re-adding documents...")
        
        from langchain_core.documents import Document
        
        docs_to_add = []
        for i in range(len(documents)):
            doc = Document(
                page_content=documents[i],
                metadata=metadatas[i] if metadatas else {}
            )
            docs_to_add.append(doc)
        
        # Add in batches of 100
        batch_size = 100
        for i in range(0, len(docs_to_add), batch_size):
            batch = docs_to_add[i:i+batch_size]
            new_store.add_documents(batch)
            print(f"   Added batch {i//batch_size + 1}/{(len(docs_to_add)-1)//batch_size + 1}")
        
        # Step 6: Verify
        final_count = new_store._collection.count()
        print(f"   ✅ Migration complete! Final count: {final_count}")
        
        if final_count != doc_count:
            print(f"   ⚠️  WARNING: Document count mismatch! (Before: {doc_count}, After: {final_count})")
            return False
        
        return True
    
    except Exception as e:
        print(f"   ❌ Migration failed: {e}")
        return False

def migrate_all_collections():
    """Migrate all collections to cosine similarity"""
    
    print("=" * 70)
    print("CHROMADB MIGRATION TO COSINE SIMILARITY")
    print("=" * 70)
    
    if not os.path.exists(CHROMA_PATH):
        print(f"\n❌ ChromaDB path not found: {CHROMA_PATH}")
        return
    
    print(f"\n📂 ChromaDB path: {CHROMA_PATH}")
    
    # Initialize embeddings (must match your existing embeddings)
    print("\n🔄 Loading embeddings model...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Get all collections
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collections = client.list_collections()
    
    if not collections:
        print("\n✅ No collections found.")
        return
    
    print(f"\n📋 Found {len(collections)} collection(s) to migrate:")
    for col in collections:
        print(f"   - {col.name}: {col.count()} documents")
    
    # Confirm
    print("\n" + "=" * 70)
    print("⚠️  This will recreate all collections with cosine similarity.")
    print("Your data will be preserved, but this may take a few minutes.")
    print("=" * 70)
    
    confirm = input("\nType 'MIGRATE' to proceed: ")
    
    if confirm != "MIGRATE":
        print("\n❌ Aborted.")
        return
    
    # Migrate each collection
    print("\n🚀 Starting migration...")
    
    success_count = 0
    fail_count = 0
    
    for col in collections:
        success = migrate_collection_to_cosine(col.name, embeddings)
        if success:
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("MIGRATION SUMMARY")
    print("=" * 70)
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print("\n" + "=" * 70)
    print("NEXT STEPS:")
    print("=" * 70)
    print("1. Restart your FastAPI server")
    print("2. Test queries - they should now work correctly!")
    print("3. Relevance scores should be 0.0 to 1.0 (not negative)")
    print("=" * 70)

if __name__ == "__main__":
    migrate_all_collections()
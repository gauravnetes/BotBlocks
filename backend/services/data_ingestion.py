"""
Enhanced Data Ingestion Service
================================
Supports:
- PDF/TXT file uploads (existing)
- Web scraping (new)
- Text content ingestion (new)
"""

import os
import time
import requests
import tempfile
from typing import Optional, Dict, Any
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from core.config import settings

# Use environment variable for path (supports Docker/Vultr) or fallback to temp
CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(tempfile.gettempdir(), "botblocks_chroma_db"))

# ============================================================================
# EXISTING FILE UPLOAD FUNCTIONS (UNCHANGED)
# ============================================================================

def ingest_from_url(bot_id: str, file_url: str, filename: str):
    """
    Downloads file from Cloudinary (or any URL) to a temp file,
    ingests it, and then cleans up.
    """
    print(f"--- DOWNLOADING & INDEXING: {filename} ---")
    
    try:
        res = requests.get(file_url)
        if res.status_code != 200:
            print(f"Failed to download file: {file_url}")
            return False
        
        # Create temp file with correct extension
        suffix = os.path.splitext(filename)[1]
        if not suffix: 
            suffix = ".tmp"
            
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(res.content)
            temp_path = tmp.name
            
    except Exception as e:
        print(f"Download Error: {e}")
        return False
    
    # Process the temp file
    success = ingest_file_from_path(temp_path, bot_id, original_filename=filename)
    
    # Cleanup the download
    if os.path.exists(temp_path):
        try:
            os.remove(temp_path)
        except:
            pass
        
    return success

def ingest_file_from_path(file_path: str, bot_id: str, original_filename: str = None):
    """
    Reads a local file, chunks it, and saves vectors to ChromaDB.
    """
    if not original_filename:
        original_filename = os.path.basename(file_path)
        
    print(f"--- STARTING INGESTION for Bot {bot_id} ({original_filename}) ---")
    start_time = time.time()
    
    # 1. Load Documents
    documents = []
    try:
        # Check extensions (Case-insensitive)
        if file_path.lower().endswith(".pdf"):
            loader = PyMuPDFLoader(file_path)
            documents.extend(loader.load())
        elif file_path.lower().endswith(".txt"):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        else:
            print(f"Unsupported file type: {file_path}")
            return False
        
        print(f"📖 Loaded {len(documents)} pages in {time.time() - start_time:.2f}s")
        
    except Exception as e:
        print(f"Error loading file: {e}")
        return False
    
    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200,  # ✅ Increased from 1000 for better context
        chunk_overlap=250,  # ✅ Increased from 200
        add_start_index=True,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    
    # 3. Add Metadata
    for doc in chunks:
        doc.metadata["source"] = original_filename
        doc.metadata["bot_id"] = bot_id
        doc.metadata["type"] = "file"  # ✅ New: Distinguish from web content

    # 4. Embed & Store
    print("Generating embeddings with BGE-small model...")
    # 4. Embed & Store
    print("Generating embeddings with BGE-small model...")
    try:           
        embeddings = get_embeddings_model()
        
        collection_name = f"collection_{bot_id}"
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        # Add documents in batches
        BATCH_SIZE = 50 
        
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i : i + BATCH_SIZE]
            vector_store.add_documents(batch)
            print(f"Processed batch {i} to {i + len(batch)}")
            
    except Exception as e:
        print(f"❌ ChromaDB Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Cleanup
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except: 
            pass
        
    total_time = time.time() - start_time 
    print(f"🎉 INGESTION COMPLETE in {total_time:.2f}s")
    return True

# ============================================================================
# NEW: TEXT CONTENT INGESTION (FOR WEB SCRAPING)
# ============================================================================

def ingest_text_content(
    bot_id: str,
    content: str,
    source_name: str,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Ingest raw text content (from web scraping or other sources)
    
    Args:
        bot_id: Bot public_id (UUID string)
        content: Raw text content
        source_name: Source identifier (e.g., "web_homepage", "web_about")
        metadata: Additional metadata (url, title, scraped_at, etc.)
    
    Returns:
        bool: Success status
    """
    print(f"--- INGESTING TEXT CONTENT for Bot {bot_id}: {source_name} ---")
    start_time = time.time()
    
    try:
        # 1. Create Document
        doc_metadata = {
            "source": source_name,
            "bot_id": bot_id,
            "type": "web"  # Mark as web-scraped content
        }
        
        # Merge additional metadata
        if metadata:
            doc_metadata.update(metadata)
        
        raw_doc = Document(
            page_content=content,
            metadata=doc_metadata
        )
        
        print(f"📄 Content length: {len(content)} characters")
        
        # 2. Split into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=250,
            add_start_index=True,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = text_splitter.split_documents([raw_doc])
        print(f"Split into {len(chunks)} chunks")
        
        # 3. Setup embeddings and vector store
        embeddings = get_embeddings_model()
        
        collection_name = f"collection_{bot_id}"
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=collection_name,
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        # 4. Add to vector store in batches
        BATCH_SIZE = 50
        
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i : i + BATCH_SIZE]
            vector_store.add_documents(batch)
            print(f"Processed batch {i} to {i + len(batch)}")
        
        total_time = time.time() - start_time
        print(f"🎉 TEXT INGESTION COMPLETE in {total_time:.2f}s")
        return True
    
    except Exception as e:
        print(f"❌ Text Ingestion Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# ============================================================================
# EXISTING UTILITY FUNCTIONS (ENHANCED)
# ============================================================================

def get_embeddings_model():
    """
    Centralized embedding model loader with error handling.
    Fixes 'meta tensor' issues by enforcing CPU safeload.
    """
    try:
        # Prevent potential recursion or meta device issues
        return HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu', 'trust_remote_code': True},
            encode_kwargs={'normalize_embeddings': True}
        )
    except Exception as e:
        print(f"⚠️ Embedding Load Error: {e}. Retrying...")
        # Fallback if specific kwargs fail
        return HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")


def list_bot_files(bot_id: str):
    """
    Returns unique sources stored in the vector database.
    Now includes both files and web sources.
    """
    try:
        embeddings = get_embeddings_model()
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings, 
            collection_name=f"collection_{bot_id}",
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        # Get metadata
        data = vector_store.get(include=["metadatas"])
        
        sources = []
        seen = set()
        
        for meta in data["metadatas"]:
            if meta and "source" in meta:
                source_name = meta["source"]
                
                # Skip duplicates
                if source_name in seen:
                    continue
                
                seen.add(source_name)
                
                # Build source info
                source_info = {
                    "name": source_name,
                    "type": meta.get("type", "file"),  # "file" or "web"
                }
                
                # Add web-specific metadata
                if meta.get("type") == "web":
                    source_info["url"] = meta.get("url", "")
                    source_info["title"] = meta.get("title", "")
                    source_info["scraped_at"] = meta.get("scraped_at", "")
                
                sources.append(source_info)
        
        return sources
    
    except Exception as e:
        print(f"List Error: {e}")
        return []

def delete_bot_source(bot_id: str, source_name: str):
    """
    Deletes all vectors associated with a specific source (file or web page).
    Renamed from delete_bot_file to be more generic.
    """
    try:
        embeddings = get_embeddings_model()
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings, 
            collection_name=f"collection_{bot_id}",
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        print(f"🗑️ Deleting vectors for source: {source_name}")
        
        vector_store._collection.delete(where={"source": source_name})
        return True
    
    except Exception as e:
        print(f"Delete Error: {e}")
        return False

# Backward compatibility alias
delete_bot_file = delete_bot_source

# ============================================================================
# NEW: WEB SCRAPING STATISTICS
# ============================================================================

def get_collection_stats(bot_id: str) -> Dict[str, Any]:
    """
    Get statistics about the bot's knowledge base
    """
    try:
        embeddings = get_embeddings_model()
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings,
            collection_name=f"collection_{bot_id}",
            collection_metadata={"hnsw:space": "cosine"}
        )
        
        data = vector_store.get(include=["metadatas"])
        
        total_chunks = len(data["metadatas"])
        file_count = 0
        web_count = 0
        
        for meta in data["metadatas"]:
            if meta:
                if meta.get("type") == "web":
                    web_count += 1
                else:
                    file_count += 1
        
        return {
            "total_chunks": total_chunks,
            "file_chunks": file_count,
            "web_chunks": web_count,
            "sources": len(list_bot_files(bot_id))
        }
    
    except Exception as e:
        print(f"Stats Error: {e}")
        return {
            "total_chunks": 0,
            "file_chunks": 0,
            "web_chunks": 0,
            "sources": 0
        }
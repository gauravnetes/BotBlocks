import os
import time
import shutil
import requests
import tempfile
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from core.config import settings

# Use environment variable for path (supports Docker/Vultr) or fallback to temp
CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(tempfile.gettempdir(), "botblocks_chroma_db"))

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
        if not suffix: suffix = ".tmp"
            
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
        chunk_size=1000, 
        chunk_overlap=200, 
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    
    # 3. Add Metadata
    for doc in chunks:
        doc.metadata["source"] = original_filename
        doc.metadata["bot_id"] = bot_id

    # 4. Embed & Store
    print("Generating embeddings locally (CPU)...")
    try:           
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Batch size 50 is safe for most CPUs
        BATCH_SIZE = 50 
        
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i : i + BATCH_SIZE]
            Chroma.from_documents(
                documents=batch,
                embedding=embeddings,
                persist_directory=CHROMA_PATH,
                collection_name=f"collection_{bot_id}"
            )
            print(f"Processed batch {i} to {i + len(batch)}")
            
    except Exception as e:
        print(f"❌ ChromaDB Error: {e}")
        return False

    # Note: ingest_from_url handles its own cleanup, but this is a safety net
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except: 
            pass
        
    total_time = time.time() - start_time 
    print(f"🎉 INGESTION COMPLETE in {total_time:.2f}s")
    return True

def list_bot_files(bot_id: str):
    """
    Returns unique filenames stored in the vector database.
    """
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        vector_store = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings, 
            collection_name=f"collection_{bot_id}"
        )
        
        # Get metadata
        data = vector_store.get(include=["metadatas"])
        
        unique_files = set()
        for meta in data["metadatas"]:
            if meta and "source" in meta:
                unique_files.add(meta["source"])
                
        return list(unique_files)
    
    except Exception as e:
        print(f"List Error: {e}")
        return []
    
def delete_bot_file(bot_id: str, filename: str):
    """
    Deletes all vectors associated with a specific file.
    """
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        vector_store = Chroma(
            persist_directory=CHROMA_PATH, 
            embedding_function=embeddings, 
            collection_name=f"collection_{bot_id}"
        )
        
        print(f"🗑️ Deleting vectors for file: {filename}")
        
        vector_store._collection.delete(where={"source": filename})
        return True
    
    except Exception as e:
        print(f"Delete Error: {e}")
        return False
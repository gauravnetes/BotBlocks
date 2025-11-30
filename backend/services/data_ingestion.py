import os
import time
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings # <--- REMOVE THIS
from langchain_huggingface import HuggingFaceEmbeddings         # <--- ADD THIS
from langchain_chroma import Chroma
from core.config import settings

import tempfile
CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

def ingest_file_from_path(file_path: str, bot_id: str):
    # ... (Load documents logic stays the same) ...
    documents = []
    try:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
            documents.extend(loader.load())
        else:
            return False
    except Exception:
        return False
    
    # ... (Split logic stays the same) ...
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    # --- SWAP TO LOCAL EMBEDDINGS ---
    print("🧠 Generating embeddings locally (CPU)...")
    
    # This runs ON YOUR LAPTOP. No API limits.
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # We can do bigger batches now because it's local!
    BATCH_SIZE = 50 
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        Chroma.from_documents(
            documents=batch,
            embedding=embeddings,
            persist_directory=CHROMA_PATH,
            collection_name=f"collection_{bot_id}"
        )
        print(f"✅ Processed batch {i}")
    

    # Cleanup
    if os.path.exists(file_path):
        os.remove(file_path)
        
    print(f"🎉 INGESTION COMPLETE for Bot {bot_id}!")  # <--- ADD THIS LINE
    return True
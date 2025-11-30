import os
import time
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from core.config import settings

# Define where to store the vector DB
CHROMA_PATH = "./data/chroma_db"

def ingest_file_from_path(file_path: str, bot_id: str):
    """
    Reads a file from a specific path (saved by the API),
    chunks it, embeds it, and saves it to ChromaDB.
    """
    
    # --- 1. Load Documents ---
    documents = []
    
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
        documents.extend(loader.load())
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
        documents.extend(loader.load())
    else:
        print(f"Unsupported file type: {file_path}")
        return False
    
    # --- 2. Split Text ---
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        add_start_index=True
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")

    # --- 3. Embed & Store (With Batching) ---
    
    # Initialize Gemini Embeddings using key from settings
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", 
        google_api_key=settings.GOOGLE_API_KEY
    )
    
    # Batch size to prevent hitting API rate limits
    BATCH_SIZE = 10 
    total_chunks = len(chunks)

    for i in range(0, total_chunks, BATCH_SIZE):
        batch = chunks[i : i + BATCH_SIZE]
        
        # Save to ChromaDB
        Chroma.from_documents(
            documents=batch,
            embedding=embeddings,
            persist_directory=CHROMA_PATH,
            collection_name=f"collection_{bot_id}"
        )
        
        print(f"Processed batch {i} to {i + BATCH_SIZE} / {total_chunks}")
        time.sleep(1) # Sleep 1s to be nice to the API

    # --- 4. Cleanup ---
    # Delete the temp file now that we are done
    if os.path.exists(file_path):
        os.remove(file_path)
        
    return True
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from pathlib import Path

# --- 1. ROBUST ENV LOADING ---
# Get the absolute path of this file (database.py)
current_file = Path(__file__).resolve()
# Go up two levels: db/ -> backend/
backend_dir = current_file.parent.parent 
env_path = backend_dir / ".env"

print(f"🔌 Attempting to load .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# --- 2. GET DB URL ---
DATABASE_URL = os.getenv("DATABASE_URL")

# --- 3. DEBUG & FALLBACK ---
print("--------------------------------------------------")
if DATABASE_URL and "postgres" in DATABASE_URL:
    print("✅ DATABASE: Found PostgreSQL Configuration")
    # Hide password for safety logs
    safe_url = DATABASE_URL.split("@")[1] if "@" in DATABASE_URL else "..."
    print(f"   Target: ...@{safe_url}")
else:
    print("⚠️  DATABASE: URL not found or invalid.")
    print("   Falling back to local SQLite.")
    DATABASE_URL = "sqlite:///./data/persistent_db.sqlite"
print("--------------------------------------------------")

# Fix for some cloud providers using postgres:// instead of postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# SQLite needs specific args, Postgres does not
connect_args = {}
if "sqlite" in DATABASE_URL:
    connect_args = {"check_same_thread": False}

# --- 4. CREATE ENGINE ---
engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
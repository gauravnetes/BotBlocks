import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Setup path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ No DATABASE_URL found.")
    exit()

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

def add_column(engine, table, column, type_def):
    try:
        with engine.connect() as conn:
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {type_def}"))
            conn.commit()
            print(f"✅ Added column {column}")
    except Exception as e:
        if "duplicate column" in str(e):
            print(f"ℹ️ Column {column} already exists.")
        else:
            print(f"❌ Error adding {column}: {e}")

if __name__ == "__main__":
    print("🚀 Updating Postgres Schema...")
    engine = create_engine(DATABASE_URL)
    
    # Add new columns for dynamic widget
    add_column(engine, "bots", "theme_color", "VARCHAR DEFAULT '#0f766e'")
    add_column(engine, "bots", "initial_message", "TEXT DEFAULT 'Hello! How can I help you today?'")
    add_column(engine, "bots", "bot_avatar", "VARCHAR DEFAULT '🤖'")
    
    print("✨ Schema Update Complete.")
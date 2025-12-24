import os
import sys
import sqlite3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 1. Setup Environment - Ensure we can find the 'db' module
# Add the backend root directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(parent_dir)

try:
    from db.models import Base, Bot
except ImportError:
    # If running from scripts folder, try one level up
    sys.path.append(os.path.dirname(parent_dir))
    from db.models import Base, Bot

load_dotenv()

# --- CONFIGURATION ---
# Logic to find the SQLite file depending on where you run the script from
if os.path.exists("./data/persistent_db.sqlite"):
    SQLITE_FILE = "./data/persistent_db.sqlite"
elif os.path.exists("../data/persistent_db.sqlite"):
    SQLITE_FILE = "../data/persistent_db.sqlite"
else:
    # Fallback to absolute path assumption
    SQLITE_FILE = os.path.join(parent_dir, "data", "persistent_db.sqlite")

SQLITE_URL = f"sqlite:///{SQLITE_FILE}"
POSTGRES_URL = os.getenv("DATABASE_URL")

if POSTGRES_URL and POSTGRES_URL.startswith("postgres://"):
    POSTGRES_URL = POSTGRES_URL.replace("postgres://", "postgresql://", 1)

def patch_sqlite_schema():
    print(f"🔍 Checking local SQLite schema at {SQLITE_FILE}...")
    
    if not os.path.exists(SQLITE_FILE):
        return

    conn = sqlite3.connect(SQLITE_FILE)
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA table_info(bots)")
    columns = [info[1] for info in cursor.fetchall()]
    
    if "allowed_origin" not in columns:
        print("   ⚠️ Column 'allowed_origin' missing. Patching SQLite file...")
        try:
            cursor.execute("ALTER TABLE bots ADD COLUMN allowed_origin TEXT DEFAULT '*'")
            conn.commit()
            print("   ✅ Column added successfully.")
        except Exception as e:
            print(f"   ❌ Failed to patch database: {e}")
    
    conn.close()

def migrate():
    if not os.path.exists(SQLITE_FILE):
        print(f"❌ SQLite file not found at {SQLITE_FILE}.")
        return

    if not POSTGRES_URL or "sqlite" in POSTGRES_URL:
        print("❌ DATABASE_URL is not pointing to a Cloud Database.")
        return

    patch_sqlite_schema()

    print("\n🚀 Starting Migration to Cloud...")
    print(f"   Source: {SQLITE_URL}")
    print(f"   Target: Neon PostgreSQL")

    # 3. Connect to Databases (The FIX is here)
    # Source (SQLite)
    sqlite_engine = create_engine(SQLITE_URL)
    SqliteSessionLocal = sessionmaker(bind=sqlite_engine)
    source_session = SqliteSessionLocal() # <--- Explicitly create instance with ()

    # Dest (Postgres)
    pg_engine = create_engine(POSTGRES_URL)
    PgSessionLocal = sessionmaker(bind=pg_engine)
    dest_session = PgSessionLocal() # <--- Explicitly create instance with ()

    # 4. Ensure Target Tables Exist
    print("   🔨 Creating tables in PostgreSQL if they don't exist...")
    Base.metadata.create_all(pg_engine)

    # 5. Transfer Data
    try:
        # Now this will work because source_session is a real Session object
        bots = source_session.query(Bot).all()
        print(f"   📦 Found {len(bots)} bots to migrate.")

        count = 0
        for bot in bots:
            exists = dest_session.query(Bot).filter_by(public_id=bot.public_id).first()
            if exists:
                print(f"      ⏭️  Skipping {bot.name} (Already migrated)")
                continue

            new_bot = Bot(
                public_id=bot.public_id,
                name=bot.name,
                system_prompt=bot.system_prompt,
                platform=bot.platform,
                platform_token=bot.platform_token,
                allowed_origin=bot.allowed_origin,
                created_at=bot.created_at
            )
            dest_session.add(new_bot)
            count += 1
        
        dest_session.commit()
        print(f"\n   🎉 SUCCESS: Migrated {count} bots to Neon!")

    except Exception as e:
        print(f"   ❌ Migration Failed: {e}")
        dest_session.rollback()
    finally:
        source_session.close()
        dest_session.close()

if __name__ == "__main__":
    migrate()
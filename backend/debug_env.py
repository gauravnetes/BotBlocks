import os
from pathlib import Path
from dotenv import load_dotenv

# 1. Determine where we are
current_dir = Path.cwd()
print(f"📍 Current Working Directory: {current_dir}")

# 2. Look for .env file
env_path = current_dir / ".env"
print(f"🔍 Looking for .env at: {env_path}")

if env_path.exists():
    print("✅ Found .env file!")
    
    # 3. Load it
    load_dotenv(dotenv_path=env_path)
    
    # 4. Check Variable
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        print(f"✅ DATABASE_URL found: {db_url[:20]}...") # Print first 20 chars for privacy
        if "sqlite" in db_url:
            print("⚠️ WARNING: It is set to SQLite!")
        elif "postgres" in db_url:
            print("🎉 SUCCESS: It is pointing to PostgreSQL!")
    else:
        print("❌ ERROR: .env exists, but DATABASE_URL is missing inside it.")
        print("   Please check spelling. It must be exactly: DATABASE_URL=...")
else:
    print("❌ ERROR: .env file NOT found.")
    print("   Make sure you created a file named '.env' (no extension) in the backend folder.")
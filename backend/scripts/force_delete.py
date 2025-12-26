"""
Nuclear option: Delete EVERYTHING and start fresh
"""

import os
import tempfile
import shutil

CHROMA_PATH = os.path.join(tempfile.gettempdir(), "botblocks_chroma_db")

print("=" * 70)
print("⚠️  NUCLEAR OPTION: DELETE ALL CHROMA DATA")
print("=" * 70)

if not os.path.exists(CHROMA_PATH):
    print("\n✅ No ChromaDB found. Nothing to delete.")
    exit()

print(f"\nPath: {CHROMA_PATH}")
print("\n⚠️  This will DELETE ALL bot training data!")
print("You will need to re-upload all documents.")

confirm = input("\nType 'NUKE' to confirm: ")

if confirm != "NUKE":
    print("\n❌ Aborted.")
    exit()

print("\n💣 Deleting ChromaDB...")
shutil.rmtree(CHROMA_PATH)

print("✅ Deleted!")
print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. Make sure your rag_pipeline.py has the cosine fix")
print("2. Restart your server")
print("3. Re-upload ALL documents")
print("4. New collections will be created correctly")
print("=" * 70)
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ No API Key found in .env file.")
    print("Please make sure you have created the .env file in the backend folder.")
    exit()

# Configure the SDK
genai.configure(api_key=api_key)

print("🔍 Checking available models for your API Key...")
print("-" * 40)

try:
    found_any = False
    for m in genai.list_models():
        # We only care about models that can generate text (chat)
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ {m.name}")
            print(f"   Description: {m.description[:60]}...")
            found_any = True
            
    if not found_any:
        print("⚠️ No text generation models found. Check your API key permissions.")
        
except Exception as e:
    print(f"❌ Error contacting Google API: {e}")
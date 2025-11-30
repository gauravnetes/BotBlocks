import requests
import streamlit as st
from botblocks_app.utils import get_backend_url

BASE_URL = get_backend_url()

def create_bot(name: str, system_prompt: str, platform: str = "web", platform_token: str = None):
    
    """POST /bots/create"""
    
    url = f"{BASE_URL}/bots/create"
    payload = {
        "name": name, 
        "system_prompt": system_prompt, 
        "platform": platform, 
        "platform_token": platform_token,
    }
    try:
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json() # Returns the bot object with public_id
    except Exception as e:
        st.error(f"Failed to create bot: {e}")
        return None
    
    
def upload_knowledge(bot_id: str, file_obj):
    
    """POST /bots/{id}/upload"""
    
    url = f"{BASE_URL}/bots/{bot_id}/upload"
    # Streamlit file_uploader object needs to be formatted for requests
    files = {"file": (file_obj.name, file_obj, file_obj.type)}
    try:
        res = requests.post(url, files=files)
        res.raise_for_status()
        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False
    

def get_all_bots():
    
    """GET /bots/"""
    
    url = f"{BASE_URL}/bots/"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return []
    except Exception:
        return []
    
    
def chat_with_bot(bot_id: str, message: str):
    
    """POST /chat/web"""
    
    url = f"{BASE_URL}/chat/web"
    payload = {"bot_id": bot_id, "message": message}
    try:
        res = requests.post(url, json=payload)
        if res.status_code == 200:
            return res.json()["response"]
        else:
            return "Error: Bot is offline."
    except Exception as e:
        return f"Connection Error: {e}"
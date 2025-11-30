import os
import json
import requests
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

BACKEND_URL = os.getenv("BOTBLOCKS_BACKEND", "http://localhost:8000")
API_PREFIX = "/api/v1"

DEMO_MODE = False

DEMO_BOTS = []

def enable_demo_mode():
    global DEMO_MODE
    DEMO_MODE = True

def is_demo_mode() -> bool:
    return DEMO_MODE

def api_get(path: str, params: Optional[Dict] = None, timeout: int = 10) -> Dict[str, Any]:
    if DEMO_MODE:
        return _demo_get_response(path, params)
    
    try:
        url = f"{BACKEND_URL}{API_PREFIX}{path}"
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        enable_demo_mode()
        return _demo_get_response(path, params)
    except requests.exceptions.Timeout:
        raise Exception(f"Request timed out after {timeout} seconds. Please check your backend connection.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

def api_post_json(path: str, json_data: Dict[str, Any], timeout: int = 30) -> Dict[str, Any]:
    if DEMO_MODE:
        return _demo_post_response(path, json_data)
    
    try:
        url = f"{BACKEND_URL}{API_PREFIX}{path}"
        r = requests.post(url, json=json_data, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        enable_demo_mode()
        return _demo_post_response(path, json_data)
    except requests.exceptions.Timeout:
        raise Exception(f"Request timed out after {timeout} seconds. Please check your backend connection.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

def api_post_multipart(path: str, files: Dict[str, Tuple], data: Optional[Dict] = None, timeout: int = 120) -> Dict[str, Any]:
    if DEMO_MODE:
        return _demo_post_response(path, {"files": True})
    
    try:
        url = f"{BACKEND_URL}{API_PREFIX}{path}"
        r = requests.post(url, files=files, data=data or {}, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        enable_demo_mode()
        return _demo_post_response(path, {"files": True})
    except requests.exceptions.Timeout:
        raise Exception(f"Request timed out after {timeout} seconds. Please check your backend connection.")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP Error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise Exception(f"Unexpected error: {str(e)}")

def _demo_get_response(path: str, params: Optional[Dict] = None) -> Dict[str, Any]:
    if "/bots/" in path and path.endswith("/bots"):
        return {"bots": DEMO_BOTS}
    
    if "/bots/" in path:
        public_id = path.split("/bots/")[1].split("/")[0]
        bot = next((b for b in DEMO_BOTS if b["public_id"] == public_id), None)
        if bot:
            return {"bot": bot}
        return {"error": "Bot not found"}
    
    return {"status": "demo_mode"}

def _demo_post_response(path: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
    global DEMO_BOTS
    
    if "/bots/create" in path:
        new_bot = {
            "id": len(DEMO_BOTS) + 1,
            "public_id": f"bot_{len(DEMO_BOTS) + 1}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": json_data.get("name", "Untitled Bot"),
            "platform": json_data.get("platform", "website"),
            "system_prompt": json_data.get("system_prompt", ""),
            "description": json_data.get("description", ""),
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "last_indexed": None,
            "documents_count": 0
        }
        DEMO_BOTS.append(new_bot)
        return {"bot": new_bot}
    
    if "/documents" in path:
        return {"status": "uploaded", "message": "Document uploaded successfully (demo mode)"}
    
    if "/index" in path:
        return {"status": "completed", "message": "Indexing completed (demo mode)"}
    
    if "/persona" in path:
        return {"status": "updated", "message": "Persona updated (demo mode)"}
    
    if "/platform" in path:
        return {"status": "updated", "message": "Platform configured (demo mode)"}
    
    if "/chat" in path:
        return {
            "reply": "This is a demo response. Connect to a real backend to see actual bot responses!",
            "sources": [
                {"id": "demo_1", "text": "Sample source document snippet", "score": 0.95}
            ],
            "actions": {}
        }
    
    if "/blocks" in path:
        return {"status": "updated", "message": "Block updated (demo mode)"}
    
    return {"status": "success", "message": "Operation completed (demo mode)"}

def validate_bot_name(name: str) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "Bot name cannot be empty"
    if len(name) < 3:
        return False, "Bot name must be at least 3 characters"
    if len(name) > 100:
        return False, "Bot name must be less than 100 characters"
    return True, ""

def validate_telegram_token(token: str) -> Tuple[bool, str]:
    if not token or not token.strip():
        return False, "Telegram token cannot be empty"
    parts = token.split(":")
    if len(parts) != 2:
        return False, "Invalid Telegram token format (should be: bot_id:hash)"
    return True, ""

def validate_discord_token(token: str) -> Tuple[bool, str]:
    if not token or not token.strip():
        return False, "Discord token cannot be empty"
    if len(token) < 50:
        return False, "Discord token seems too short"
    return True, ""

def validate_url(url: str) -> Tuple[bool, str]:
    if not url or not url.strip():
        return False, "URL cannot be empty"
    if not url.startswith(("http://", "https://")):
        return False, "URL must start with http:// or https://"
    return True, ""

def format_datetime(dt_string: Optional[str]) -> str:
    if not dt_string:
        return "Never"
    try:
        dt = datetime.fromisoformat(dt_string.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return dt_string

def save_draft(draft_data: Dict[str, Any]) -> bool:
    try:
        with open("/tmp/botblocks_draft.json", "w") as f:
            json.dump(draft_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Failed to save draft: {e}")
        return False

def load_draft() -> Optional[Dict[str, Any]]:
    try:
        if os.path.exists("/tmp/botblocks_draft.json"):
            with open("/tmp/botblocks_draft.json", "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"Failed to load draft: {e}")
    return None

def clear_draft() -> bool:
    try:
        if os.path.exists("/tmp/botblocks_draft.json"):
            os.remove("/tmp/botblocks_draft.json")
        return True
    except Exception as e:
        print(f"Failed to clear draft: {e}")
        return False

def get_backend_url() -> str:
    return BACKEND_URL

def get_persona_options() -> List[Dict[str, str]]:
    return [
        {
            "id": "friendly",
            "name": "Friendly",
            "description": "Warm, approachable, and conversational",
            "prompt": "You are a friendly and helpful assistant. Be warm, approachable, and conversational in your responses."
        },
        {
            "id": "professional",
            "name": "Professional",
            "description": "Formal, precise, and business-oriented",
            "prompt": "You are a professional assistant. Be formal, precise, and business-oriented in your responses."
        },
        {
            "id": "witty",
            "name": "Witty",
            "description": "Clever, humorous, and engaging",
            "prompt": "You are a witty assistant with a good sense of humor. Be clever, engaging, and occasionally humorous in your responses."
        },
        {
            "id": "energetic",
            "name": "Energetic",
            "description": "Enthusiastic, motivating, and upbeat",
            "prompt": "You are an energetic and enthusiastic assistant! Be motivating, upbeat, and inspiring in your responses."
        },
        {
            "id": "custom",
            "name": "Custom",
            "description": "Define your own persona",
            "prompt": ""
        }
    ]

def get_platform_options() -> List[Dict[str, str]]:
    return [
        {
            "id": "website",
            "name": "Website",
            "description": "Embed on your website with a chat widget",
            "icon": "🌐"
        },
        {
            "id": "telegram",
            "name": "Telegram",
            "description": "Deploy as a Telegram bot",
            "icon": "💬"
        },
        {
            "id": "discord",
            "name": "Discord",
            "description": "Deploy as a Discord bot",
            "icon": "🎮"
        }
    ]

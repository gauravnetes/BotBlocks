import uuid 
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any

class BotBase(BaseModel):
    name: str
    system_prompt: Optional[str] = "You are a helpful assistant."
    platform: str = "web"
    platform_token: Optional[str] = None
    allowed_origin: Optional[str] = "*" 
    
    theme_color: Optional[str] = "#0f766e"
    initial_message: Optional[str] = "Hello! How can I help you today?"
    bot_avatar: Optional[str] = "🤖"
    
class BotCreate(BotBase): 
    pass 

class BotConfigUpdate(BaseModel):
    theme_color: Optional[str] = None
    initial_message: Optional[str] = None
    bot_avatar: Optional[str] = None
    name: Optional[str] = None

# Widget Configuration Schema
class WidgetConfig(BaseModel):
    theme: str = "modern"  # modern, classic, minimal
    primary_color: str = "#3b82f6"
    avatar_url: Optional[str] = None
    welcome_message: str = "Hello! How can I help you today?"
    bot_display_name: Optional[str] = None
    position: str = "bottom-right"  # bottom-right, bottom-left
    button_style: str = "circle"  # circle, rounded, square

class WidgetConfigUpdate(BaseModel):
    theme: Optional[str] = None
    primary_color: Optional[str] = None
    avatar_url: Optional[str] = None
    welcome_message: Optional[str] = None
    bot_display_name: Optional[str] = None
    position: Optional[str] = None
    button_style: Optional[str] = None
        
class Bot(BotBase):
    id: int
    public_id: str
    created_at: datetime
    widget_config: Optional[str] = None  # JSON string
    
    class Config:
        form_attributes = True
                
        
class ChatRequest(BaseModel):  
    bot_id: str
    message: str
    
class ChatResponse(BaseModel): 
    response: str
    sources: list = []
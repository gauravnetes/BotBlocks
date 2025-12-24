import uuid 
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

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
        
class Bot(BotBase):
    id: int
    public_id: str
    created_at: datetime
    
    class Config:
        form_attributes = True
                
        
class ChatRequest(BaseModel):  
    bot_id: str
    message: str
    
class ChatResponse(BaseModel): 
    response: str
    sources: list = []
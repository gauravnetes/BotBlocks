import uuid 
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BotBase(BaseModel):
    name: str
    system_prompt: Optional[str] = "You are a helpful assistant."
    platform: str = "web"
    platform_token: Optional[str] = None
    
class BotCreate(BotBase): 
    pass 

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
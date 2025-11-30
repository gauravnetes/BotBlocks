from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base  

class Bot(Base):
    __tablename__ = "bots"
    
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True, index=True) 
    name = Column(String, default="My Bot")
    system_prompt = Column(Text, default="You are a helpful assistant.")
    platform = Column(String) 
    platform_token = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
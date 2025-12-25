from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.sql import func
from db.database import Base  

class Bot(Base):
    __tablename__ = "bots"
    
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String, unique=True, index=True) 
    
    name = Column(String, default="My Bot")
    system_prompt = Column(Text, default="You are a helpful assistant.")
    
    platform = Column(String) 
    platform_token = Column(String, nullable=True)
    allowed_origin = Column(String, default="*")
    
    # widget appearance (legacy fields - keeping for backwards compatibility)
    # theme_color = Column(String, default="#0f766e")
    # initial_message = Column(Text, default = "Hello! How can I help you today?")
    # bot_avatar = Column(String, default="🤖")
    
    # New widget configuration (JSON)
    widget_config = Column(Text, default='{"theme": "modern", "primary_color": "#3b82f6", "avatar_url": null, "welcome_message": "Hello! How can I help you today?", "bot_display_name": null, "position": "bottom-right", "button_style": "circle"}')
    
    health_score = Column(Float, default=100.0)
    last_health_check_at = Column(DateTime(timezone=True), nullable=True)
    
    cached_insight_summary = Column(Text, nullable=True)
    last_insight_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(String, index=True)
    
    filename = Column(String)
    cloudinary_url = Column(String)
    cloudinary_public_id = Column(String)
    file_type = Column(String)
    file_size = Column(Integer)
    
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    
class BotAuditLog(Base):
    __tablename__ = "bot_audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    bot_id = Column(Integer, ForeignKey("bots.id"))
    
    user_query = Column(String)
    bot_response = Column(String)
    confidence_score = Column(Float)
    
    flagged_as_gap = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
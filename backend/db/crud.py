import uuid 
from sqlalchemy.orm import Session
from . import models, schemas

def get_bot(db: Session, bot_id: int):
    return db.query(models.Bot).filter(models.Bot.id == bot_id).first()

def get_bot_by_public_id(db: Session, public_id: str):
    return db.query(models.Bot).filter(models.Bot.public_id == public_id).first()

def get_bots(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bot).offset(skip).limit(limit).all()

def create_bot(db: Session, bot: schemas.BotCreate): 
    public_id = str(uuid.uuid4())
    
    db_bot = models.Bot(
        public_id = public_id, 
        name = bot.name,
        system_prompt = bot.system_prompt, 
        platform = bot.platform, 
        platform_token = bot.platform_token, 
        allowed_origin = bot.allowed_origin,
        
        theme_color = bot.theme_color,
        initial_message = bot.initial_message, 
        bot_avatar = bot.bot_avatar
    )
    
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot

def update_bot_config(db: Session, public_id: str, config: schemas.BotConfigUpdate):
    
    db_bot = get_bot_by_public_id(db, public_id)
    if not db_bot:
        return None
    
    if config.theme_color: 
        db_bot.theme_color = config.theme_color
    if config.initial_message:
        db_bot.initial_message = config.initial_message
    if config.bot_avatar:
        db_bot.bot_avatar = config.bot_avatar
    if config.name:
        db_bot.name = config.name
        
    db.commit()
    db.refresh()
    return db_bot

def delete_bot(db: Session, public_id: str):
    
    db_bot = get_bot_by_public_id(db, public_id)
    if db_bot:
        db.delete(db_bot)
        db.commit()
        return True
    return False
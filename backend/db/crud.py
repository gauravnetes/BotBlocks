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
        platform_token = bot.platform_token
    )
    
    db.add(db_bot)
    db.commit()
    db.refresh(db_bot)
    return db_bot
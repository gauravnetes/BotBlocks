from sqlalchemy.orm import Session
from fastapi import UploadFile
from db import models
import cloudinary.uploader

def upload_asset(db: Session, bot_public_id: str, file: UploadFile):
    """
    Upload asset and associate with bot
    
    Args:
        bot_public_id: Bot's public_id (UUID string)
        file: Uploaded file
    """
    try:
        # ✅ First, get the bot to access its integer ID
        bot = db.query(models.Bot).filter(
            models.Bot.public_id == bot_public_id
        ).first()
        
        if not bot:
            print(f"Bot not found: {bot_public_id}")
            return None
        
        # ✅ Use bot.id (integer) instead of bot_public_id (string)
        existing = db.query(models.Asset).filter_by(
            bot_id=bot.id,  # ✅ Changed from bot_public_id
            filename=file.filename
        ).first()
        
        if existing:
            return existing
        
        res = cloudinary.uploader.upload(
            file.file,
            folder=f"botblocks/{bot_public_id}",  # Keep using public_id for folder name
            resource_type="raw",
            use_filename=True,
            unique_filename=False
        )
        
        new_asset = models.Asset(
            bot_id=bot.id,  # ✅ Changed from bot_public_id
            filename=file.filename,
            cloudinary_url=res.get("secure_url"),
            cloudinary_public_id=res.get("public_id"),
            file_type=file.filename.split('.')[-1],
            file_size=res.get("bytes")
        )
        
        db.add(new_asset)
        db.commit()
        db.refresh(new_asset)
        
        return new_asset
    
    except Exception as e:
        print(f"Cloudinary Upload Error: {e}")
        db.rollback()
        return None


def list_assets(db: Session, bot_public_id: str):
    """List all assets for a bot"""
    # ✅ Get bot first
    bot = db.query(models.Bot).filter(
        models.Bot.public_id == bot_public_id
    ).first()
    
    if not bot:
        return []
    
    # ✅ Use bot.id
    assets = db.query(models.Asset).filter(
        models.Asset.bot_id == bot.id
    ).all()
    
    return [
        {
            "id": asset.id,
            "filename": asset.filename,
            "file_type": asset.file_type,
            "file_size": asset.file_size,
            "cloudinary_url": asset.cloudinary_url,
            "uploaded_at": asset.uploaded_at.isoformat()
        }
        for asset in assets
    ]


def delete_asset(db: Session, bot_public_id: str, filename: str):
    """Delete an asset"""
    try:
        # ✅ Get bot first
        bot = db.query(models.Bot).filter(
            models.Bot.public_id == bot_public_id
        ).first()
        
        if not bot:
            return False
        
        # ✅ Use bot.id
        asset = db.query(models.Asset).filter(
            models.Asset.bot_id == bot.id,
            models.Asset.filename == filename
        ).first()
        
        if not asset:
            return False
        
        # Delete from Cloudinary
        if asset.cloudinary_public_id:
            try:
                cloudinary.uploader.destroy(
                    asset.cloudinary_public_id,
                    resource_type="raw"
                )
            except Exception as e:
                print(f"Cloudinary delete error: {e}")
        
        # Delete from database
        db.delete(asset)
        db.commit()
        
        return True
    
    except Exception as e:
        print(f"Delete asset error: {e}")
        db.rollback()
        return False


def get_asset(db: Session, bot_public_id: str, filename: str):
    """Get a specific asset"""
    bot = db.query(models.Bot).filter(
        models.Bot.public_id == bot_public_id
    ).first()
    
    if not bot:
        return None
    
    return db.query(models.Asset).filter(
        models.Asset.bot_id == bot.id,
        models.Asset.filename == filename
    ).first()
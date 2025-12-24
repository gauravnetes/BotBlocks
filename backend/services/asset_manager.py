import os
import shutil
import cloudinary
import cloudinary.uploader
from sqlalchemy.orm import Session
from db import models
from dotenv import load_dotenv

from fastapi import UploadFile
from typing import List

load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"), 
    api_secret = os.getenv("CLOUDINARY_API_SECRET"), 
    secure = True
)

def upload_asset(db: Session, bot_id: str, file: UploadFile):
    
    try: 
        existing = db.query(models.Asset).filter_by(bot_id=bot_id, filename = file.filename).first()
        if existing: 
            return existing
        
        res = cloudinary.uploader.upload(
            file.file, 
            folders=f"botblocks/{bot_id}", 
            resource_type="raw", 
            use_filename=True, 
            unique_filename=False
        )
        
        new_asset = models.Asset(
            bot_id=bot_id, 
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
        return None
    
def delete_asset(db: Session, bot_id: str, filename: str):
    
    asset = db.query(models.Asset).filter_by(bot_id=bot_id, filename=filename).first()
    if not asset:
        return False
    
    try:
        
        cloudinary.uploader.destroy(asset.cloudinary_public_id,  resouce_type="raw")
        
        db.delete(asset)
        db.commit()
        return True
    
    except Exception as e:
        print(f"Cloudinary Delete Error: {e}")
        return False
    

def list_assets(db: Session, bot_id: str):
    assets = db.query(models.Asset).filter_by(bot_id=bot_id).all()
    return [a.filename for a in assets]

def get_asset_url(db: Session, bot_id: str, filename: str):
    asset = db.query(models.Asset).filter_by(bot_id=bot_id, filename=filename).first()
    return asset.cloudinary_url if asset else None
        

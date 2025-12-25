import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from fastapi.responses import RedirectResponse

from db import crud, schemas
from db.database import get_db
from services import data_ingestion, asset_manager


router = APIRouter(
    prefix="/api/v1/bots",
    tags=["Bots"]
)

@router.post("/create", response_model=schemas.Bot)
def create_new_bot(bot: schemas.BotCreate, db: Session = Depends(get_db)):
    # Check if a bot with this name already exists (optional safety check)
    # existing_bot = db.query(models.Bot).filter(models.Bot.name == bot.name).first()
    # if existing_bot: ...
    
    new_bot = crud.create_bot(db=db, bot=bot)
    return new_bot

@router.get("/{public_id}", response_model=schemas.Bot)
def read_bot(public_id: str, db: Session = Depends(get_db)):
    db_bot = crud.get_bot_by_public_id(db, public_id=public_id)
    if db_bot is None:
        raise HTTPException(status_code=404, detail="Bot not found")
    return db_bot

@router.get("/", response_model=List[schemas.Bot])
def read_all_bots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    bots = crud.get_bots(db, skip=skip, limit=limit)
    return bots

def process_upload_background(file_path: str, bot_id: str):

    try:
        data_ingestion.ingest_file_from_path(file_path, bot_id)
    except Exception as e:
        print(f"Background Ingestion Failed for {bot_id}: {e}")
        # In a real app, you'd mark the bot status as 'Failed' in the DB here.

@router.post("/{public_id}/upload")
async def upload_knowledge(
    public_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # 1. Verify Bot Exists
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    asset = asset_manager.upload_asset(db, public_id, file)
    if not asset:
        raise HTTPException(status_code=500, detail="Failed to upload asset")
    
    # 2. Save Temp File
    # Create temp directory
    # temp_dir = f"./data/temp/{public_id}"
    # os.makedirs(temp_dir, exist_ok=True)
    
    # # Define full path
    # temp_file_path = f"{temp_dir}/{file.filename}"
    
    # # Write bytes to disk
    # with open(temp_file_path, "wb") as buffer:
    #     shutil.copyfileobj(file.file, buffer)

    # 3. Queue Background Task
    background_tasks.add_task(
        data_ingestion.ingest_from_url,         
        public_id, 
        asset.cloudinary_url, 
        asset.filename
    )

    return {"message": "File uploaded to Cloud & Indexing started."}


@router.delete("/{public_id}")
def delete_existing_bot(public_id: str, db: Session = Depends(get_db)):
    """
    Delete a bot.
    """
    success = crud.delete_bot(db, public_id)
    if not success:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Optional: You could also try to delete the Chroma collection here,
    # but for a hackathon, leaving the vector files is safer to avoid "File Lock" crashes.
    
    return {"message": "Bot deleted successfully"}

@router.get("/{public_id}/config")
def get_bot_widget_config(public_id: str, db: Session = Depends(get_db)):
    
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot: 
        raise HTTPException(status_code=404, detail="Bot Not Found")
    

    return {
        "bot_name": bot.name, 
        "theme_color": bot.theme_color, 
        "initiala_message": bot.initial_message, 
        "bot_avatar": bot.bot_avatar
    }
    
    
@router.patch("/{public_id}/config", response_model=schemas.Bot)
def update_bot_visuals(
    public_id: str, 
    config: schemas.BotConfigUpdate, 
    db: Session = Depends(get_db)
):
    updated_bot = crud.update_bot_config(db, public_id, config)
    if not updated_bot:
        raise HTTPException(status_code=404, detail="Bot Not Found")
    
    return updated_bot

@router.get("/{public_id}/files")
def get_bot_files(public_id: str, db: Session = Depends(get_db)):
    
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot Not Found")
    
    files = data_ingestion.list_bot_files(public_id)
    return {"files": files}

@router.delete("/{public_id}/files/{filename}")
def delete_bot_file(public_id: str, filename: str, db: Session = Depends(get_db)):
    
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot Not Found")
    
    success = data_ingestion.delete_bot_file(public_id, filename)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete File")
    
    return {"message": f"File {filename} deleted successfully"}

import requests
from fastapi.responses import StreamingResponse

import mimetypes

@router.get("/{public_id}/files/{filename}/download")
def download_file(public_id: str, filename: str, inline: bool = False, db: Session = Depends(get_db)):
    url = asset_manager.get_asset_url(db, public_id, filename)
    if not url:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Proxy the download to set headers
    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
        
        disposition = "inline" if inline else "attachment"
        
        # Explicitly guess mime type to force browser preview
        content_type, _ = mimetypes.guess_type(filename)
        if not content_type:
            content_type = r.headers.get("Content-Type", "application/octet-stream")
            
        # Force text/plain for .txt/md files to ensure they display
        if filename.endswith(".txt") or filename.endswith(".md"):
             content_type = "text/plain"
        
        return StreamingResponse(
            r.iter_content(chunk_size=1024),
            media_type=content_type,
            headers={"Content-Disposition": f'{disposition}; filename="{filename}"'}
        )
    except Exception as e:
        print(f"Proxy download failed: {e}")
        # Fallback to redirect if proxy fails
        return RedirectResponse(url)

# ===== WIDGET CONFIGURATION ENDPOINTS =====

@router.get("/{public_id}/widget-config")
def get_widget_configuration(public_id: str, db: Session = Depends(get_db)):
    """
    Public endpoint to get widget configuration (used by embedded widget)
    """
    import json
    
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Parse widget_config JSON
    try:
        widget_config = json.loads(bot.widget_config) if bot.widget_config else {}
    except json.JSONDecodeError:
        # Fallback to default if JSON is invalid
        widget_config = {
            "theme": "modern",
            "primary_color": "#3b82f6",
            "avatar_url": None,
            "welcome_message": "Hello! How can I help you today?",
            "bot_display_name": None,
            "position": "bottom-right",
            "button_style": "circle"
        }
    
    # Override with bot name if display name not set
    if not widget_config.get("bot_display_name"):
        widget_config["bot_display_name"] = bot.name
    
    return widget_config

@router.put("/{public_id}/widget-config")
def update_widget_configuration(
    public_id: str,
    config: schemas.WidgetConfigUpdate,
    db: Session = Depends(get_db)
):
    """
    Update widget configuration
    """
    import json
    
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    # Get current config
    try:
        current_config = json.loads(bot.widget_config) if bot.widget_config else {}
    except json.JSONDecodeError:
        current_config = {}
    
    # Update only provided fields
    update_data = config.dict(exclude_unset=True)
    current_config.update(update_data)
    
    # Save back as JSON string
    updated_bot = crud.update_widget_config(db, public_id, json.dumps(current_config))
    
    if not updated_bot:
        raise HTTPException(status_code=500, detail="Failed to update configuration")
    
    return {"message": "Widget configuration updated successfully", "config": current_config}
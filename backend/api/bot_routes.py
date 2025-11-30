import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from db import crud, schemas
from db.database import get_db
from services import data_ingestion

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

# --- NEW: Background Upload Handler ---
def process_upload_background(file_path: str, bot_id: str):
    """
    Background task wrapper.
    """
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
    """
    Upload a PDF/TXT file. 
    1. Saves file to disk immediately.
    2. Starts ingestion in background.
    3. Returns 'Success' immediately.
    """
    # 1. Verify Bot Exists
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # 2. Save Temp File
    # Create temp directory
    temp_dir = f"./data/temp/{public_id}"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Define full path
    temp_file_path = f"{temp_dir}/{file.filename}"
    
    # Write bytes to disk
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 3. Queue Background Task
    background_tasks.add_task(
        process_upload_background, 
        temp_file_path, 
        public_id
    )

    return {"message": "File received! AI training started in the background."}

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
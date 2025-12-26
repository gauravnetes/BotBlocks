from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from db import models
# Import your existing asset manager
from services import asset_manager
# Import RAG service to process the file content
from services import rag_pipeline 
import requests
import logging
from api.deps import get_current_user

logger = logging.getLogger("KnowledgeRouter")

router = APIRouter(prefix="/api/v1/bots", tags=["Knowledge Base"])

@router.post("/{bot_id}/knowledge-base/upload")
async def upload_knowledge(
    bot_id: str, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    bot = db.query(models.Bot).filter(models.Bot.public_id == bot_id).first()
    if not bot: raise HTTPException(404, "Bot Not Found")

    if bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # We pass the public_id (bot_id) to asset_manager
    asset = asset_manager.upload_asset(db, bot_id, file)
    if not asset:
        raise HTTPException(500, "Failed to Upload Asset")
    
    try:
        # Download the text from Cloudinary
        # Note: This works for .txt/.md files directly. 
        # For PDFs, you'll need a PDF parser (PyPDF2) here. 
        # Assuming Text for now as per "manual entry" discussion.
        response = requests.get(asset.cloudinary_url)
        response.raise_for_status()
        
        file_content = ""
        
        # PDF Handling 
        if asset.filename.endswith(".pdf"):
             import fitz
             
             with fitz.open(stream=response.content, filetype="pdf") as doc:
                 for page in doc:
                     file_content += page.get_text()
        else:
             # Regular Text
             file_content = response.text

        # Inject into RAG
        if not file_content.strip():
            logger.warning(f"File {asset.filename} seems empty or unreadable.")
        else:
            rag_pipeline.add_document_to_knowledge_base(bot_id, file_content, asset.filename)
        
    except Exception as e:
        logger.error(f"Training Failed: {e}")
        # We don't fail the request because the file IS saved. 
        # We just return a warning status.
        return {
            "status": "partial_success", 
            "message": "File saved, but training failed. Please retry.",
            "error": str(e)
        }

    return {"status": "success", "filename": asset.filename, "message": "Bot trained successfully."}


@router.get("/{bot_id}/knowledge-base")
def list_knowledge(
    bot_id: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verify bot exists
    bot = db.query(models.Bot).filter(models.Bot.public_id == bot_id).first()
    if not bot: raise HTTPException(404, "Bot Not Found")

    if bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    files = asset_manager.list_assets(db, bot_id)
    return {"files": files}


@router.delete("/{bot_id}/knowledge-base/{filename}")
def delete_knowledge(
    bot_id: str, 
    filename: str, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    
    bot = db.query(models.Bot).filter(models.Bot.public_id == bot_id).first()
    if not bot: raise HTTPException(404, "Bot Not Found")

    if bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    success = asset_manager.delete_asset(db, bot_id, filename)
    if not success:
        raise HTTPException(404, "File not found")
        
    rag_pipeline.remove_document_from_knowledge_base(bot_id, filename)
    
    return {"status": "deleted"}
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import schemas, crud
from db.database import get_db

from services import rag_pipeline

router = APIRouter(
    prefix="/api/v1/chat", 
    tags=["Chat"]
)

@router.post("/web", response_model=schemas.ChatResponse)
def chat_with_bot(
    chat_request: schemas.ChatRequest, 
    db: Session = Depends(get_db)
): 
    bot = crud.get_bot_by_public_id(db, public_id=chat_request.bot_id)
    if not bot: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bot not Found"
        )
        
    try: 
        ans = rag_pipeline.generate_response(
            message=chat_request.message, 
            bot=bot
        )
        
    except Exception as e:
        print(f"Error in RAG Pipeline: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Something went wrong generating the response"
        )  
        
    return schemas.ChatResponse(response=ans)
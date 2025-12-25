from fastapi import APIRouter, Depends, HTTPException, status, Request
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
    request: Request,
    chat_request: schemas.ChatRequest, 
    db: Session = Depends(get_db)
): 
    
    bot = crud.get_bot_by_public_id(db, public_id=chat_request.bot_id)
    if not bot: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Bot not Found"
        )
    
    request_origin = request.headers.get("origin")
    
    
    if bot.allowed_origin and bot.allowed_origin != "*":
        if not request_origin:
            print(f"Warning: No origin Header. Bot requires {bot.allowed_origin}")
            
            # PRODUCTION:
            # raise HTTPException(status_code=403, detail="Origin header missing")
            
        elif bot.allowed_origin not in request_origin:
            print(print(f"Security Alert: Blocked request from {request_origin} for bot {bot.name}"))
            
            raise HTTPException(
                status_code=403, 
                detail=f"CORS Error: This bot is restricted to {bot.allowed_origin}"
            )
    
    
    try: 
        ans = rag_pipeline.generate_response(
            message=chat_request.message, 
            bot=bot,
            db=db
        )
        
    except Exception as e:
        print(f"Error in RAG Pipeline: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Something went wrong generating the response"
        )  
        
    return schemas.ChatResponse(response=ans)
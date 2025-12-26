from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from pydantic import BaseModel
import logging
from datetime import datetime

from db.database import get_db
from db import models, crud
from services import analytics_service

logger = logging.getLogger("BotAnalytics")
router = APIRouter(prefix="/api/v1/bots", tags=["analytics"])

# RESPONSE MODELS
class HealthScoreResponse(BaseModel):
    bot_id: str
    health_score: float
    last_checked: str = None

class KnowledgeGapStatsResponse(BaseModel):
    total_queries: int
    failed_queries: int
    low_confidence_queries: int
    success_rate: float
    avg_confidence: float
    period_days: int

# ============================================================================
# HELPER: Get Bot ID by Public ID
# ============================================================================
def get_bot_id(public_id: str, db: Session) -> int:
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return bot.id

# ============================================================================
# COMPREHENSIVE ANALYTICS (DASHBOARD)
# ============================================================================
@router.get("/{public_id}/analytics/comprehensive")
async def get_comprehensive_analytics(
    public_id: str,
    db: Session = Depends(get_db)
):
    """
    Get all analytics data in one call.
    """
    bot_id = get_bot_id(public_id, db)
    try:
        data = await analytics_service.get_comprehensive_insights(bot_id, db)
        return data  # Return directly to match frontend interface
    except Exception as e:
        logger.error(f"Dashboard data retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load dashboard data")

# ============================================================================
# REFRESH INSIGHTS
# ============================================================================
@router.post("/{public_id}/analytics/refresh-insights")
async def refresh_insights(
    public_id: str,
    db: Session = Depends(get_db)
):
    """
    Force refresh AI insights.
    """
    bot_id = get_bot_id(public_id, db)
    try:
        # We await this synchronously for the "Refersh" button experience, 
        # or we could make it BG task. 
        # Frontend expects new data back immediately or polling.
        # But smart_insights might be slow (LLM). 
        # Let's try to wait for it since it uses a "spinner" on frontend.
        insights = await analytics_service.get_smart_insights(bot_id, db, force_refresh=True)
        
        # Return full updated dashboard data so frontend can update everything
        data = await analytics_service.get_comprehensive_insights(bot_id, db)
        return data
        
    except Exception as e:
        logger.error(f"Insight refresh failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# GAP STATISTICS
# ============================================================================
@router.get("/{public_id}/analytics/gaps")
def get_gap_stats(
    public_id: str,
    days: int = 7,
    db: Session = Depends(get_db)
):
    bot_id = get_bot_id(public_id, db)
    stats = analytics_service.get_knowledge_gap_stats(bot_id, db, days=days)
    return stats

# ============================================================================
# RESOLVE GAP (ADD KNOWLEDGE)
# ============================================================================
class ResolveGapRequest(BaseModel):
    query: str
    answer: str
    log_id: int | None = None  # Optional, if we want to resolve a specific log entry

@router.post("/{public_id}/analytics/resolve-gap")
async def resolve_gap(
    public_id: str,
    request: ResolveGapRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Resolve a knowledge gap by adding a Q&A pair and marking logs as resolved.
    """
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
        
    try:
        # 1. Add to Knowledge Base (RAG)
        # Create a Q&A format text
        qa_content = f"Question: {request.query}\nAnswer: {request.answer}"
        filename = f"quick_fix_{request.query[:10].replace(' ', '_')}_{str(datetime.now().timestamp())}.txt"
        
        # We use the RAG pipeline directly to add this 'document'
        from services import rag_pipeline
        success = rag_pipeline.add_document_to_knowledge_base(bot.public_id, qa_content, filename)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to add knowledge to vector store")
            
        # 2. Mark specific log as resolved (if provided) or find matching ones
        if request.log_id:
            log = db.query(models.BotAuditLog).filter(models.BotAuditLog.id == request.log_id).first()
            if log:
                log.is_resolved = True
        
        # Also resolve other pending gaps that match this query text exactly
        # This cleans up the "Top Failed" list immediately
        pending_logs = db.query(models.BotAuditLog)\
            .filter(models.BotAuditLog.bot_id == bot.id)\
            .filter(models.BotAuditLog.user_query == request.query)\
            .filter(models.BotAuditLog.flagged_as_gap == True)\
            .filter(models.BotAuditLog.is_resolved == False)\
            .all()
            
        for l in pending_logs:
            l.is_resolved = True
            
        db.commit()
        
        # 3. Recalculate Health Score immediately
        new_score = analytics_service.update_bot_health_if_needed(bot.id, db)
        
        return {
            "status": "success", 
            "message": "Knowledge added and gaps resolved",
            "new_health_score": new_score
        }
        
    except Exception as e:
        logger.error(f"Resolve gap failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

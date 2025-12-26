from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
from pydantic import BaseModel
import logging

from db.database import get_db
from db import models
from services import analytics_service

logger = logging.getLogger("BotAnalytics")
router = APIRouter(prefix="/bots", tags=["analytics"])

# RESPONSE MODELS
class HealthScoreResponse(BaseModel):
    bot_id: int
    health_score: float
    last_checked: str

class KnowledgeGapStatsResponse(BaseModel):
    total_queries: int
    failed_queries: int
    low_confidence_queries: int
    success_rate: float
    avg_confidence: float
    period_days: int

class InsightRefreshRequest(BaseModel):
    force_refresh: bool = False

# HEALTH SCORE ENDPOINT
@router.get("/{bot_id}/health", response_model=HealthScoreResponse)
def get_bot_health(
    bot_id: int,
    db: Session = Depends(get_db)
):
    """
    Get bot health score (0-100).
    Cached for 24 hours.
    
    Health Score Formula: (1 - FailureRate) * 100
    - 100: Perfect - no knowledge gaps
    - 70-99: Good - minor gaps
    - 50-69: Fair - needs training
    - <50: Poor - significant gaps
    """
    try:
        bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        health_score = analytics_service.update_bot_health_if_needed(bot_id, db)
        
        return HealthScoreResponse(
            bot_id=bot_id,
            health_score=health_score,
            last_checked=bot.last_health_check_at.isoformat() if bot.last_health_check_at else None
        )
    
    except Exception as e:
        logger.error(f"Health check failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to calculate health score")

# ============================================================================
# KNOWLEDGE GAP STATISTICS
# ============================================================================
@router.get("/{bot_id}/stats", response_model=KnowledgeGapStatsResponse)
def get_knowledge_gap_stats(
    bot_id: int,
    days: int = 7,
    db: Session = Depends(get_db)
):
    """
    Get detailed knowledge gap statistics.
    
    Parameters:
    - bot_id: Bot identifier
    - days: Time period to analyze (default: 7 days)
    """
    try:
        bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        stats = analytics_service.get_knowledge_gap_stats(bot_id, db, days=days)
        return KnowledgeGapStatsResponse(**stats)
    
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")

# ============================================================================
# AI-POWERED INSIGHTS
# ============================================================================
@router.get("/{bot_id}/insights")
async def get_knowledge_gap_insights(
    bot_id: int,
    force_refresh: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get AI-powered knowledge gap analysis.
    
    Returns clustered topics of missing knowledge with:
    - Topic name
    - Number of related queries
    - Sample queries
    - Advice on what to add
    - Priority level (high/medium/low)
    
    Results are cached for 24 hours unless force_refresh=True.
    """
    try:
        bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        insights = await analytics_service.get_smart_insights(bot_id, db, force_refresh)
        
        return {
            "bot_id": bot_id,
            "insights": insights,
            "cached_at": bot.last_insight_at.isoformat() if bot.last_insight_at else None,
            "total_topics": len(insights)
        }
    
    except Exception as e:
        logger.error(f"Insights generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to generate insights")

# ============================================================================
# RECENT KNOWLEDGE GAPS
# ============================================================================
@router.get("/{bot_id}/gaps/recent")
def get_recent_gaps(
    bot_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Get recent queries that failed (knowledge gaps).
    Useful for quick dashboard view.
    
    Parameters:
    - limit: Number of recent gaps to return (default: 20, max: 100)
    """
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
    
    try:
        bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        gaps = analytics_service.get_recent_knowledge_gaps(bot_id, db, limit=limit)
        
        return {
            "bot_id": bot_id,
            "gaps": gaps,
            "count": len(gaps)
        }
    
    except Exception as e:
        logger.error(f"Recent gaps retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve recent gaps")

# ============================================================================
# TOP FAILED QUERIES
# ============================================================================
@router.get("/{bot_id}/gaps/top")
def get_top_failed_queries(
    bot_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get most frequently asked questions that failed.
    Helps prioritize what knowledge to add first.
    
    Returns queries sorted by frequency (last 30 days).
    """
    try:
        bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        top_queries = analytics_service.get_top_failed_queries(bot_id, db, limit=limit)
        
        return {
            "bot_id": bot_id,
            "top_failed_queries": top_queries,
            "period": "last_30_days"
        }
    
    except Exception as e:
        logger.error(f"Top queries retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve top queries")

# ============================================================================
# COMPREHENSIVE DASHBOARD DATA
# ============================================================================
@router.get("/{bot_id}/dashboard")
async def get_dashboard_data(
    bot_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all analytics data in one call - optimized for dashboard.
    
    Returns:
    - Health score
    - 7-day statistics
    - AI-powered insights
    - Recent knowledge gaps (10)
    - Top failed queries (10)
    """
    try:
        bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        data = await analytics_service.get_comprehensive_insights(bot_id, db)
        
        return {
            "bot_id": bot_id,
            "bot_name": bot.name,
            "data": data
        }
    
    except Exception as e:
        logger.error(f"Dashboard data retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to load dashboard data")

# ============================================================================
# BACKGROUND TASK FOR PERIODIC INSIGHT GENERATION
# ============================================================================
@router.post("/{bot_id}/insights/refresh")
async def refresh_insights_background(
    bot_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Trigger background insight generation.
    Useful for scheduled tasks or manual refresh.
    
    Returns immediately with task confirmation.
    Insights will be available after processing completes.
    """
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    async def refresh_task():
        try:
            logger.info(f"Background task: Refreshing insights for bot {bot_id}")
            await analytics_service.get_smart_insights(bot_id, db, force_refresh=True)
            logger.info(f"Background task: Insights refresh completed for bot {bot_id}")
        except Exception as e:
            logger.error(f"Background insight refresh failed: {e}")
    
    background_tasks.add_task(refresh_task)
    
    return {
        "status": "queued",
        "message": "Insight generation queued. Check back in a few moments.",
        "bot_id": bot_id
    }

# ============================================================================
# AUDIT LOG QUERY
# ============================================================================
@router.get("/{bot_id}/audit-logs")
def get_audit_logs(
    bot_id: int,
    limit: int = 50,
    gaps_only: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get raw audit logs for debugging or export.
    
    Parameters:
    - limit: Number of logs to return (max: 200)
    - gaps_only: If true, only return queries flagged as knowledge gaps
    """
    if limit > 200:
        raise HTTPException(status_code=400, detail="Limit cannot exceed 200")
    
    try:
        bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
        if not bot:
            raise HTTPException(status_code=404, detail="Bot not found")
        
        query = db.query(models.BotAuditLog)\
            .filter(models.BotAuditLog.bot_id == bot_id)
        
        if gaps_only:
            query = query.filter(models.BotAuditLog.flagged_as_gap == True)
        
        logs = query.order_by(models.BotAuditLog.created_at.desc())\
            .limit(limit)\
            .all()
        
        return {
            "bot_id": bot_id,
            "logs": [
                {
                    "id": log.id,
                    "query": log.user_query,
                    "response": log.bot_response,
                    "confidence": log.confidence_score,
                    "flagged_as_gap": log.flagged_as_gap,
                    "timestamp": log.created_at.isoformat()
                }
                for log in logs
            ],
            "count": len(logs),
            "filters": {"gaps_only": gaps_only}
        }
    
    except Exception as e:
        logger.error(f"Audit log retrieval failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve audit logs")
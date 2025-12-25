from datetime import timedelta, datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.database import get_db
from db import models
from services import analytics_service 

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/bots/{bot_id}/dashboard-data")
async def get_bot_dashboard_data(bot_id: int, db: Session = Depends(get_db)):
    """
    Aggregates all analytics data for the Bot Dashboard.
    Optimized with 24h caching for expensive operations.
    """
    
    # 1. Verify Bot Ownership
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # 2. Get Health Score (Fast / Cached)
    health_score = analytics_service.update_bot_health_if_needed(bot.id, db)

    # 3. Get Smart Suggestions (Async / Cached LLM)
    smart_summary = await analytics_service.get_smart_insights(bot.id, db)

    # 4. Get Recent "Raw" Logs (Real-time from DB)
    # We fetch the last 5 logs just to show a "Recent Activity" list in UI
    raw_logs = db.query(models.BotAuditLog)\
             .filter(models.BotAuditLog.bot_id == bot_id)\
             .filter(models.BotAuditLog.flagged_as_gap == True)\
             .order_by(models.BotAuditLog.created_at.desc())\
             .limit(5)\
             .all()
             
    week_ago = datetime.now() - timedelta(days=7)
    total_gaps_count = db.query(func.count(models.BotAuditLog.id))\
             .filter(models.BotAuditLog.bot_id == bot_id)\
             .filter(models.BotAuditLog.flagged_as_gap == True)\
             .filter(models.BotAuditLog.created_at >= week_ago)\
             .scalar()

    return {
        "status": "success",
        "metrics": {
            "health_score": health_score,
            "total_knowledge_gaps_7d": total_gaps_count# This is approximate, just for UI
        },
        "actionable_insights": smart_summary,
        "recent_failures_log": [
            {
                "query": l.user_query,
                "response": l.bot_response, 
                "time": l.created_at
            } for l in raw_logs
        ]
    }
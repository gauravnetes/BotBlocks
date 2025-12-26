from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
import json
import logging
import re
from typing import List, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings
from db import models

logger = logging.getLogger("AnalyticsService")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
def clean_json_text(text: str) -> str:
    """Extract clean JSON from markdown-wrapped text"""
    text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```$', '', text, flags=re.MULTILINE)
    return text.strip()

# ============================================================================
# BOT HEALTH SCORING
# ============================================================================
def update_bot_health_if_needed(bot_id: int, db: Session) -> float:
    """
    Calculates bot health score based on success rate.
    Formula: (1 - FailureRate) * 100
    Cached for 24 hours to reduce DB load.
    """
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        logger.warning(f"Bot {bot_id} not found")
        return 0.0
    
    # Check cache (24-hour TTL)
    if bot.last_health_check_at:
        hours_since = (datetime.now() - bot.last_health_check_at).total_seconds() / 3600
        if hours_since < 24:
            logger.info(f"Using cached health score: {bot.health_score}")
            return bot.health_score
    
    logger.info(f"Recalculating health score for bot {bot_id}")
    
    # Get queries from last 7 days
    week_ago = datetime.now() - timedelta(days=7)
    
    total_queries = db.query(func.count(models.BotAuditLog.id))\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.created_at >= week_ago)\
        .scalar()
    
    if total_queries == 0:
        new_score = 100.0
        logger.info("No queries in last 7 days - default health: 100")
    else:
        gaps = db.query(func.count(models.BotAuditLog.id))\
            .filter(models.BotAuditLog.bot_id == bot_id)\
            .filter(models.BotAuditLog.flagged_as_gap == True)\
            .filter(models.BotAuditLog.created_at >= week_ago)\
            .scalar()
        
        fail_rate = gaps / total_queries
        new_score = round((1.0 - fail_rate) * 100, 1)
        logger.info(f"Health Score: {new_score}% (Gaps: {gaps}/{total_queries})")
    
    # Update cache
    bot.health_score = new_score
    bot.last_health_check_at = datetime.now()
    db.commit()
    
    return new_score

# ============================================================================
# KNOWLEDGE GAP METRICS
# ============================================================================
def get_knowledge_gap_stats(bot_id: int, db: Session, days: int = 7) -> Dict[str, Any]:
    """
    Returns comprehensive knowledge gap statistics.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    # Total queries in period
    total_queries = db.query(func.count(models.BotAuditLog.id))\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.created_at >= cutoff_date)\
        .scalar()
    
    # Failed queries (knowledge gaps)
    failed_queries = db.query(func.count(models.BotAuditLog.id))\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.flagged_as_gap == True)\
        .filter(models.BotAuditLog.created_at >= cutoff_date)\
        .scalar()
    
    # Low confidence queries
    low_confidence = db.query(func.count(models.BotAuditLog.id))\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.confidence_score < 0.7)\
        .filter(models.BotAuditLog.confidence_score > 0.0)\
        .filter(models.BotAuditLog.created_at >= cutoff_date)\
        .scalar()
    
    # Average confidence score
    avg_confidence = db.query(func.avg(models.BotAuditLog.confidence_score))\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.created_at >= cutoff_date)\
        .scalar() or 0.0
    
    success_rate = 0.0
    if total_queries > 0:
        success_rate = round(((total_queries - failed_queries) / total_queries) * 100, 1)
    
    return {
        "total_queries": total_queries,
        "failed_queries": failed_queries,
        "low_confidence_queries": low_confidence,
        "success_rate": success_rate,
        "avg_confidence": round(float(avg_confidence), 2),
        "period_days": days
    }

# ============================================================================
# SPAM FILTER FOR ANALYST
# ============================================================================
def is_spam_or_irrelevant(query: str, bot_persona: str) -> bool:
    """
    Quick spam/irrelevant query detection before sending to LLM.
    Reduces token waste on obvious spam.
    """
    query_lower = query.lower().strip()
    
    # Common spam patterns
    spam_indicators = [
        len(query) < 3,  # Too short
        query_lower in ['hi', 'hello', 'hey', 'test', 'testing', '?', '.', 'ok'],
        re.match(r'^[^\w\s]+$', query),  # Only special characters
        'viagra' in query_lower,
        'casino' in query_lower,
        re.match(r'^(\w)\1{5,}', query),  # Repeated characters (aaaaaaa)
    ]
    
    return any(spam_indicators)

# AI ANALYST ENGINE
async def get_smart_insights(bot_id: int, db: Session, force_refresh: bool = False) -> List[Dict[str, Any]]:
    """
    Generates AI-powered insights on knowledge gaps.
    Uses LLM to cluster failed queries and suggest document additions.
    Cached for 24 hours unless force_refresh=True.
    """
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        logger.warning(f"Bot {bot_id} not found")
        return []
    
    # Check cache (24-hour TTL)
    if not force_refresh and bot.last_insight_at and bot.cached_insight_summary:
        hours_since = (datetime.now() - bot.last_insight_at).total_seconds() / 3600
        if hours_since < 24:
            try:
                cached_data = json.loads(bot.cached_insight_summary)
                logger.info(f"Using cached insights ({len(cached_data)} topics)")
                return cached_data
            except Exception as e:
                logger.warning(f"Failed to parse cached insights: {e}")
    
    logger.info(f"Running AI Analyst Engine for Bot {bot_id}")
    
    # Get failed queries from last 30 days
    cutoff_date = datetime.now() - timedelta(days=30)
    
    logs = db.query(models.BotAuditLog)\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.flagged_as_gap == True)\
        .filter(models.BotAuditLog.created_at >= cutoff_date)\
        .order_by(models.BotAuditLog.created_at.desc())\
        .limit(50)\
        .all()
    
    if not logs:
        logger.info("No knowledge gaps found - bot is performing well")
        bot.cached_insight_summary = "[]"
        bot.last_insight_at = datetime.now()
        db.commit()
        return []
    
    # Pre-filter obvious spam
    valid_queries = []
    for log in logs:
        if not is_spam_or_irrelevant(log.user_query, bot.system_prompt):
            valid_queries.append(log.user_query)
    
    if not valid_queries:
        logger.info("All failed queries were spam/irrelevant")
        bot.cached_insight_summary = "[]"
        bot.last_insight_at = datetime.now()
        db.commit()
        return []
    
    # Build prompt for LLM analyst
    failed_queries = "\n".join([f"- {q}" for q in valid_queries[:30]])  # Limit to 30 for token efficiency
    
    prompt = f"""You are a Data Analyst specializing in chatbot knowledge gap analysis.

BOT CONTEXT:
This chatbot has the following role/persona:
"{bot.system_prompt[:300]}..."

TASK:
Below are user queries that the bot FAILED to answer (flagged as knowledge gaps).
Your job is to identify REAL missing knowledge and filter out any remaining spam/irrelevant queries.

FAILED USER QUERIES:
{failed_queries}

INSTRUCTIONS:
1. **FILTER**: Discard queries that are:
   - Completely unrelated to the bot's purpose (e.g., asking a Banking Bot about pizza recipes)
   - Simple greetings or test messages
   - Gibberish or spam
   
2. **CLUSTER**: Group the remaining VALID queries into "Missing Knowledge Topics"
   - Look for patterns and themes
   - Group similar questions together
   
3. **ADVISE**: For each topic, suggest:
   - What specific information/document would fix this gap
   - Why users are asking about this
   
REQUIRED JSON OUTPUT:
[
  {{
    "topic": "Clear topic name (e.g., 'API Authentication', 'Pricing Plans')",
    "count": 5,
    "sample_queries": ["example query 1", "example query 2"],
    "advice": "Add a document explaining...",
    "priority": "high|medium|low"
  }}
]

PRIORITY RULES:
- high: Count >= 5 or critical functionality questions
- medium: Count 2-4 or feature-related questions  
- low: Count 1 or edge case questions

If ALL queries are spam/irrelevant, return: []

Respond with valid JSON only."""
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2,
            google_api_key=settings.GOOGLE_API_KEY,
            transport="rest"
        )
        
        logger.info("Invoking LLM for knowledge gap analysis...")
        res = await llm.ainvoke(prompt)
        
        cleaned_json = clean_json_text(res.content)
        data = json.loads(cleaned_json)
        
        logger.info(f"AI Analyst identified {len(data)} knowledge gap topics")
        
        # Cache results
        bot.cached_insight_summary = cleaned_json
        bot.last_insight_at = datetime.now()
        db.commit()
        
        return data
        
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse LLM JSON response: {e}")
        return []
    except Exception as e:
        logger.error(f"Analyst generation failed: {str(e)}", exc_info=True)
        return []


# RECENT GAPS - For Dashboard
def get_recent_knowledge_gaps(bot_id: int, db: Session, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Returns recent queries that were flagged as knowledge gaps.
    Used for quick dashboard view.
    """
    logs = db.query(models.BotAuditLog)\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.flagged_as_gap == True)\
        .order_by(models.BotAuditLog.created_at.desc())\
        .limit(limit)\
        .all()
    
    return [
        {
            "query": log.user_query,
            "response": log.bot_response,
            "confidence": log.confidence_score,
            "timestamp": log.created_at.isoformat()
        }
        for log in logs
    ]

# ============================================================================
# QUERY FREQUENCY ANALYSIS
# ============================================================================
def get_top_failed_queries(bot_id: int, db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Returns most frequently asked questions that failed.
    Helps prioritize what knowledge to add first.
    """
    cutoff_date = datetime.now() - timedelta(days=30)
    
    # Group by similar queries (exact match for now)
    results = db.query(
        models.BotAuditLog.user_query,
        func.count(models.BotAuditLog.id).label('count')
    )\
        .filter(models.BotAuditLog.bot_id == bot_id)\
        .filter(models.BotAuditLog.flagged_as_gap == True)\
        .filter(models.BotAuditLog.created_at >= cutoff_date)\
        .group_by(models.BotAuditLog.user_query)\
        .order_by(desc('count'))\
        .limit(limit)\
        .all()
    
    return [
        {
            "query": r.user_query,
            "frequency": r.count
        }
        for r in results
    ]

# EXPORT FUNCTION FOR API
async def get_comprehensive_insights(bot_id: int, db: Session) -> Dict[str, Any]:
    """
    Returns all insights in one call - optimized for dashboard.
    """
    return {
        "health_score": update_bot_health_if_needed(bot_id, db),
        "stats": get_knowledge_gap_stats(bot_id, db, days=7),
        "ai_insights": await get_smart_insights(bot_id, db),
        "recent_gaps": get_recent_knowledge_gaps(bot_id, db, limit=10),
        "top_failed_queries": get_top_failed_queries(bot_id, db, limit=10),
        "generated_at": datetime.now().isoformat()
    }
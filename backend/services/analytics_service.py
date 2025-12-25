from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
import json
import logging
import re
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings
from db import models

logger = logging.getLogger("AnalyticsService")

def clean_json_text(text: str) -> str:
    text = re.sub(r'^```json\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```$', '', text, flags=re.MULTILINE)
    return text.strip()

# bot health function
def update_bot_health_if_needed(bot_id: int, db: Session) -> float:
    # (1 - FailureRate) * 100
    
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot: return 0.0
    
    if bot.last_health_check_at:
        hours_since = (datetime.now() - bot.last_health_check_at).total_seconds() / 3600
        if hours_since < 24: 
            return bot.health_score
        
    week_ago = datetime.now() - timedelta(days=7)
    total_queries = db.query(func.count(models.BotAuditLog.id))\
                .filter(models.BotAuditLog.bot_id == bot_id)\
                .filter(models.BotAuditLog.created_at >= week_ago).scalar()
                    
    if total_queries == 0:
        new_score = 100.0
    else: 
        gaps = db.query(func.count(models.BotAuditLog.id))\
            .filter(models.BotAuditLog.bot_id == bot_id)\
            .filter(models.BotAuditLog.flagged_as_gap == True)\
            .filter(models.BotAuditLog.created_at >= week_ago).scalar()
            
        fail_rate = gaps / total_queries
        new_score = round((1.0 - fail_rate) * 100, 1)
        
    bot.health_score = new_score
    bot.last_health_check_at = datetime.now()
    db.commit()
    
    return new_score

# analyst engine
async def get_smart_insights(bot_id: int, db: Session) -> list: 
    
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot: return []
    
    if bot.last_insight_at and bot.cached_insight_summary:
        hours_since = (datetime.now() - bot.last_insight_at).total_seconds() / 3600
        if hours_since < 24:
            try: 
                return json.loads(bot.cached_insight_summary)
            except: 
                pass
            
    logger.info(f"Running Analyst Engine for Bot {bot_id} (Cache Expired)")
    
    logs = db.query(models.BotAuditLog)\
            .filter(models.BotAuditLog.bot_id == bot_id)\
            .filter(models.BotAuditLog.flagged_as_gap == True)\
            .order_by(models.BotAuditLog.created_at.desc())\
            .limit(30)\
            .all()
            
            
    if not logs: 
        bot.cached_insight_summary = "[]"
        bot.last_insight_at = datetime.now()
        db.commit()
        return []
    
    failed_queries = "\n".join([f"- {log.user_query}" for log in logs])
    
    prompt = f"""
    You are a strictly logical Data Analyst.
    Below is a list of questions that users asked a specific Chatbot, but the Bot failed to answer effectively (low confidence or missing data).
    
    CONTEXT:
    This bot has the following System Persona: "{bot.system_prompt[:200]}..." 
    (It is designed to answer questions related to this persona).
    
    TASK:
    Below is a list of questions users asked, but the bot failed to answer.
    Your job is to identify REAL knowledge gaps and ignore SPAM/IRRELEVANT queries.
    
    USER QUERIES: 
    {failed_queries}
    
    INSTRUCTIONS:
    1. FILTER: Discard any query that is clearly spam, gibberish, or completely unrelated to the bot's persona (e.g., asking a Banking Bot for a pizza recipe, or "hi", "test").
    2. CLUSTER: Group the remaining VALID business questions into "Missing Topics".
    3. ADVISE: Suggest a specific document/text addition for each valid topic.
    
    REQUIRED JSON STRUCTURE: 
    [
        {{
            "topic": "Topic Name (e.g., Pricing, API Keys)",
            "count": (integer) Number of rerlated queires, 
            "advice": "Add information about..."
        }}
    ]
    
    If all queries are irrelevant, return an empty list [].
    """
    
    try: 
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            temperature=0.2, 
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        res = await llm.ainvoke(prompt)
        cleaned_json = clean_json_text(res.content)
        data = json.loads(cleaned_json)
        
        bot.cached_insight_summary = cleaned_json
        bot.last_insight_at = datetime.now()
        db.commit()
        
        return data
        
    except Exception as e:
        logger.error(f"Analyst Generation Failed: {str(e)}")
        return []
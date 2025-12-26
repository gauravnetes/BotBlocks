from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import Literal
from db.database import get_db
from db import models
from services.web_scraping_service import WebScrapingService

router = APIRouter(prefix="/api/v1/bots", tags=["Web Scraping"])

# ============================================================================
# REQUEST MODELS
# ============================================================================
class SingleURLScrapeRequest(BaseModel):
    url: HttpUrl

class WebsiteScrapeRequest(BaseModel):
    start_url: HttpUrl
    method: Literal["sitemap", "crawl", "single"] = "sitemap"
    max_pages: int = 50
    max_depth: int = 2

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/{bot_id}/scrape/single")
def scrape_single_url(
    bot_id: int,
    request: SingleURLScrapeRequest,
    db: Session = Depends(get_db)
):
    """
    Scrape a single URL and add to bot's knowledge base
    """
    result = WebScrapingService.scrape_single_url(
        bot_id=bot_id,
        url=str(request.url),
        db=db
    )
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result.get('error', 'Scraping failed'))
    
    return result

@router.post("/{bot_id}/scrape/website")
def scrape_website(
    bot_id: int,
    request: WebsiteScrapeRequest,
    db: Session = Depends(get_db)
):
    """
    Scrape entire website using specified method
    """
    result = WebScrapingService.scrape_website(
        bot_id=bot_id,
        start_url=str(request.start_url),
        method=request.method,
        db=db,
        max_pages=request.max_pages,
        max_depth=request.max_depth
    )
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result.get('error', 'Scraping failed'))
    
    return result

@router.post("/{bot_id}/scrape/website/async")
def scrape_website_async(
    bot_id: int,
    request: WebsiteScrapeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Scrape website in background (for large sites)
    """
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    background_tasks.add_task(
        WebScrapingService.scrape_website,
        bot_id=bot_id,
        start_url=str(request.start_url),
        method=request.method,
        db=db,
        max_pages=request.max_pages,
        max_depth=request.max_depth
    )
    
    return {
        "success": True,
        "message": "Scraping started in background",
        "bot_id": bot_id
    }

@router.get("/{bot_id}/scrape/preview")
def preview_website_scraping(
    bot_id: int,
    url: str,
    db: Session = Depends(get_db)
):
    """
    Preview what would be scraped from a URL
    """
    from services.web_scraping_service import RequestsHelper, ContentExtractor
    
    bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    
    session = RequestsHelper.get_session()
    html = RequestsHelper.fetch_url(url, session)
    
    if not html:
        raise HTTPException(status_code=400, detail="Failed to fetch URL")
    
    extracted = ContentExtractor.extract(html, url)
    
    if not extracted:
        raise HTTPException(status_code=400, detail="Failed to extract content")
    
    return {
        "url": url,
        "title": extracted['title'],
        "content_preview": extracted['content'][:500] + "...",
        "content_length": len(extracted['content']),
        "estimated_chunks": len(extracted['content']) // 1200
    }
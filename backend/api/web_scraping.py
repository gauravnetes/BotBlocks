from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from typing import Literal
from db.database import get_db
from db import models, crud
from services.web_scraping_service import WebScrapingService
from api.deps import get_current_user

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
# HELPER: Get Bot ID with Auth
# ============================================================================
def get_bot_id_with_auth(public_id: str, db: Session, current_user: models.User) -> int:
    bot = crud.get_bot_by_public_id(db, public_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    if bot.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return bot.id

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/{public_id}/scrape/single")
def scrape_single_url(
    public_id: str,
    request: SingleURLScrapeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Scrape a single URL and add to bot's knowledge base
    """
    bot_id = get_bot_id_with_auth(public_id, db, current_user)

    result = WebScrapingService.scrape_single_url(
        bot_id=bot_id,
        url=str(request.url),
        db=db
    )
    
    if not result['success']:
        raise HTTPException(status_code=400, detail=result.get('error', 'Scraping failed'))
    
    return result

@router.post("/{public_id}/scrape/website")
def scrape_website(
    public_id: str,
    request: WebsiteScrapeRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Scrape entire website using specified method
    """
    bot_id = get_bot_id_with_auth(public_id, db, current_user)

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

@router.post("/{public_id}/scrape/website/async")
def scrape_website_async(
    public_id: str,
    request: WebsiteScrapeRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Scrape website in background (for large sites)
    """
    bot_id = get_bot_id_with_auth(public_id, db, current_user)
    
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

@router.get("/{public_id}/scrape/preview")
def preview_website_scraping(
    public_id: str,
    url: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Preview what would be scraped from a URL
    """
    # Just need ownership check, don't strictly need bot_id for preview unless logging
    get_bot_id_with_auth(public_id, db, current_user)
    
    from services.web_scraping_service import RequestsHelper, ContentExtractor
    
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
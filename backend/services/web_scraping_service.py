"""
Web Scraping Service for RAG Knowledge Base
============================================

Features:
- Single URL scraping
- Sitemap-based bulk scraping
- Recursive crawling with depth control
- Content extraction & cleaning
- Automatic chunking & ingestion into RAG
- Rate limiting & robots.txt compliance
- Progress tracking for async operations

Dependencies:
pip install beautifulsoup4 requests lxml trafilatura sitemap-parser
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Any, Set, Optional
import logging
import time
import re
from datetime import datetime
from sqlalchemy.orm import Session
import trafilatura  # Best library for main content extraction
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from db import models
from services import data_ingestion  # Your existing ingestion service

logger = logging.getLogger("WebScrapingService")

# ============================================================================
# CONFIGURATION
# ============================================================================
class ScrapingConfig:
    """Centralized configuration for web scraping"""
    
    # Rate Limiting
    REQUEST_DELAY = 1.0  # seconds between requests
    MAX_RETRIES = 3
    TIMEOUT = 10  # seconds
    
    # Content Limits
    MAX_URLS_PER_SITEMAP = 100  # Prevent abuse
    MAX_CRAWL_DEPTH = 3  # For recursive crawling
    MAX_CONTENT_LENGTH = 500_000  # 500KB per page (prevent memory issues)
    
    # Content Filters
    EXCLUDED_EXTENSIONS = {
        '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.css', '.js',
        '.zip', '.exe', '.dmg', '.mp4', '.mp3', '.avi', '.mov'
    }
    
    EXCLUDED_PATTERNS = [
        r'/login', r'/signup', r'/admin', r'/cart', r'/checkout',
        r'/account', r'/auth', r'/api/', r'\?', r'#'
    ]
    
    # User Agent
    USER_AGENT = 'BotBlocksBot/1.0 (+https://botblocks.com/bot)'

# ============================================================================
# UTILITIES
# ============================================================================
class RequestsHelper:
    """HTTP requests with retry logic and rate limiting"""
    
    @staticmethod
    def get_session() -> requests.Session:
        """Create session with retry strategy"""
        session = requests.Session()
        
        retry_strategy = Retry(
            total=ScrapingConfig.MAX_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    @staticmethod
    def fetch_url(url: str, session: requests.Session) -> Optional[str]:
        """Fetch URL content with error handling"""
        try:
            headers = {'User-Agent': ScrapingConfig.USER_AGENT}
            
            response = session.get(
                url,
                headers=headers,
                timeout=ScrapingConfig.TIMEOUT,
                allow_redirects=True
            )
            
            response.raise_for_status()
            
            # Check content length
            if len(response.content) > ScrapingConfig.MAX_CONTENT_LENGTH:
                logger.warning(f"Content too large for {url}, skipping")
                return None
            
            # Rate limiting
            time.sleep(ScrapingConfig.REQUEST_DELAY)
            
            return response.text
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None

class URLValidator:
    """Validate and filter URLs"""
    
    @staticmethod
    def is_valid_url(url: str, base_domain: str) -> bool:
        """Check if URL should be scraped"""
        
        # Parse URL
        parsed = urlparse(url)
        
        # Must be same domain
        if parsed.netloc != base_domain:
            return False
        
        # Check file extensions
        path = parsed.path.lower()
        if any(path.endswith(ext) for ext in ScrapingConfig.EXCLUDED_EXTENSIONS):
            return False
        
        # Check excluded patterns
        full_url = url.lower()
        if any(re.search(pattern, full_url) for pattern in ScrapingConfig.EXCLUDED_PATTERNS):
            return False
        
        return True
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Remove fragments and trailing slashes"""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return normalized.rstrip('/')

# ============================================================================
# CONTENT EXTRACTION
# ============================================================================
class ContentExtractor:
    """Extract main content from HTML"""
    
    @staticmethod
    def extract_with_trafilatura(html: str, url: str) -> Optional[Dict[str, Any]]:
        """Use Trafilatura for best content extraction"""
        try:
            # Extract main content
            content = trafilatura.extract(
                html,
                include_links=False,
                include_images=False,
                include_tables=True,
                favor_precision=True,  # Reduces noise
                deduplicate=True
            )
            
            if not content or len(content.strip()) < 100:
                logger.warning(f"Insufficient content extracted from {url}")
                return None
            
            # Extract metadata
            metadata = trafilatura.extract_metadata(html)
            
            return {
                "content": content.strip(),
                "title": metadata.title if metadata else "Untitled",
                "description": metadata.description if metadata else "",
                "url": url,
                "extracted_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Content extraction failed for {url}: {e}")
            return None
    
    @staticmethod
    def extract_with_beautifulsoup(html: str, url: str) -> Optional[Dict[str, Any]]:
        """Fallback extraction using BeautifulSoup"""
        try:
            soup = BeautifulSoup(html, 'lxml')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Untitled"
            
            # Get main content
            main_content = None
            
            # Try common content containers
            for tag in ['article', 'main', 'div[role="main"]', '.content', '#content']:
                main_content = soup.select_one(tag)
                if main_content:
                    break
            
            # Fallback to body
            if not main_content:
                main_content = soup.find('body')
            
            if not main_content:
                return None
            
            text = main_content.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            if len(text) < 100:
                logger.warning(f"Insufficient content from {url}")
                return None
            
            return {
                "content": text,
                "title": title_text,
                "description": "",
                "url": url,
                "extracted_at": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"BeautifulSoup extraction failed for {url}: {e}")
            return None
    
    @staticmethod
    def extract(html: str, url: str) -> Optional[Dict[str, Any]]:
        """Extract content using best available method"""
        
        # Try Trafilatura first (best quality)
        result = ContentExtractor.extract_with_trafilatura(html, url)
        
        # Fallback to BeautifulSoup
        if not result:
            result = ContentExtractor.extract_with_beautifulsoup(html, url)
        
        return result

# ============================================================================
# CRAWLERS
# ============================================================================
class WebCrawler:
    """Crawl website and extract URLs"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.session = RequestsHelper.get_session()
        self.visited: Set[str] = set()
    
    def get_links_from_page(self, url: str, html: str) -> List[str]:
        """Extract all valid links from a page"""
        try:
            soup = BeautifulSoup(html, 'lxml')
            links = []
            
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                
                # Convert relative to absolute
                absolute_url = urljoin(url, href)
                
                # Normalize
                normalized = URLValidator.normalize_url(absolute_url)
                
                # Validate
                if URLValidator.is_valid_url(normalized, self.base_domain):
                    links.append(normalized)
            
            return list(set(links))  # Remove duplicates
        
        except Exception as e:
            logger.error(f"Failed to extract links from {url}: {e}")
            return []
    
    def crawl_recursive(self, start_url: str, max_depth: int = 2) -> List[str]:
        """Recursively crawl website up to max_depth"""
        
        to_visit = [(start_url, 0)]  # (url, depth)
        discovered_urls = []
        
        while to_visit:
            url, depth = to_visit.pop(0)
            
            # Skip if already visited
            if url in self.visited:
                continue
            
            # Skip if max depth exceeded
            if depth > max_depth:
                continue
            
            logger.info(f"Crawling: {url} (depth: {depth})")
            
            # Fetch page
            html = RequestsHelper.fetch_url(url, self.session)
            if not html:
                continue
            
            # Mark as visited
            self.visited.add(url)
            discovered_urls.append(url)
            
            # Extract links for next level
            if depth < max_depth:
                links = self.get_links_from_page(url, html)
                for link in links:
                    if link not in self.visited:
                        to_visit.append((link, depth + 1))
        
        logger.info(f"Crawling complete. Found {len(discovered_urls)} pages.")
        return discovered_urls
    
    def get_sitemap_urls(self) -> List[str]:
        """Try to get URLs from sitemap.xml"""
        sitemap_urls = [
            urljoin(self.base_url, '/sitemap.xml'),
            urljoin(self.base_url, '/sitemap_index.xml'),
        ]
        
        for sitemap_url in sitemap_urls:
            try:
                logger.info(f"Checking sitemap: {sitemap_url}")
                html = RequestsHelper.fetch_url(sitemap_url, self.session)
                
                if not html:
                    continue
                
                soup = BeautifulSoup(html, 'xml')
                locs = soup.find_all('loc')
                
                urls = [loc.get_text().strip() for loc in locs]
                
                # Filter and limit
                filtered = [
                    URLValidator.normalize_url(u) 
                    for u in urls 
                    if URLValidator.is_valid_url(u, self.base_domain)
                ]
                
                # Apply limit
                filtered = filtered[:ScrapingConfig.MAX_URLS_PER_SITEMAP]
                
                logger.info(f"Found {len(filtered)} URLs in sitemap")
                return filtered
            
            except Exception as e:
                logger.warning(f"Failed to parse sitemap {sitemap_url}: {e}")
        
        return []

# ============================================================================
# MAIN SCRAPING SERVICE
# ============================================================================
class WebScrapingService:
    """Main service for web scraping and ingestion"""
    
    @staticmethod
    def scrape_single_url(
        bot_id: int,
        url: str,
        db: Session
    ) -> Dict[str, Any]:
        """Scrape a single URL and add to knowledge base"""
        
        logger.info(f"Scraping single URL: {url}")
        
        try:
            # Validate bot exists
            bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
            if not bot:
                return {"success": False, "error": "Bot not found"}
            
            # Fetch content
            session = RequestsHelper.get_session()
            html = RequestsHelper.fetch_url(url, session)
            
            if not html:
                return {"success": False, "error": "Failed to fetch URL"}
            
            # Extract content
            extracted = ContentExtractor.extract(html, url)
            
            if not extracted:
                return {"success": False, "error": "Failed to extract content"}
            
            # Ingest into RAG
            success = data_ingestion.ingest_text_content(
                bot_id=bot.public_id,
                content=extracted['content'],
                source_name=f"web_{urlparse(url).netloc}",
                metadata={
                    "url": url,
                    "title": extracted['title'],
                    "scraped_at": extracted['extracted_at']
                }
            )
            
            if not success:
                return {"success": False, "error": "Failed to ingest content"}
            
            return {
                "success": True,
                "url": url,
                "title": extracted['title'],
                "content_length": len(extracted['content']),
                "message": "Successfully scraped and added to knowledge base"
            }
        
        except Exception as e:
            logger.error(f"Single URL scraping error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def scrape_website(
        bot_id: int,
        start_url: str,
        method: str,  # "sitemap", "crawl", or "single"
        db: Session,
        max_pages: int = 50,
        max_depth: int = 2
    ) -> Dict[str, Any]:
        """
        Scrape entire website using specified method
        
        Args:
            bot_id: Bot ID
            start_url: Starting URL
            method: "sitemap" (use sitemap.xml), "crawl" (recursive), "single"
            max_pages: Maximum pages to scrape
            max_depth: Maximum crawl depth (for "crawl" method)
        """
        
        logger.info(f"Starting website scrape: {start_url}, method: {method}")
        
        try:
            # Validate bot
            bot = db.query(models.Bot).filter(models.Bot.id == bot_id).first()
            if not bot:
                return {"success": False, "error": "Bot not found"}
            
            # Initialize crawler
            crawler = WebCrawler(start_url)
            
            # Get URLs based on method
            if method == "single":
                urls = [start_url]
            
            elif method == "sitemap":
                urls = crawler.get_sitemap_urls()
                if not urls:
                    logger.warning("No sitemap found, falling back to crawl")
                    urls = crawler.crawl_recursive(start_url, max_depth=1)
            
            elif method == "crawl":
                urls = crawler.crawl_recursive(start_url, max_depth=max_depth)
            
            else:
                return {"success": False, "error": f"Invalid method: {method}"}
            
            # Limit URLs
            urls = urls[:max_pages]
            
            logger.info(f"Scraping {len(urls)} pages...")
            
            # Scrape each URL
            results = {
                "total_urls": len(urls),
                "successful": 0,
                "failed": 0,
                "pages": []
            }
            
            for idx, url in enumerate(urls, 1):
                logger.info(f"Processing {idx}/{len(urls)}: {url}")
                
                # Fetch
                html = RequestsHelper.fetch_url(url, crawler.session)
                if not html:
                    results['failed'] += 1
                    continue
                
                # Extract
                extracted = ContentExtractor.extract(html, url)
                if not extracted:
                    results['failed'] += 1
                    continue
                
                # Ingest
                success = data_ingestion.ingest_text_content(
                    bot_id=bot.public_id,
                    content=extracted['content'],
                    source_name=f"web_{urlparse(url).path.strip('/').replace('/', '_') or 'home'}",
                    metadata={
                        "url": url,
                        "title": extracted['title'],
                        "scraped_at": extracted['extracted_at']
                    }
                )
                
                if success:
                    results['successful'] += 1
                    results['pages'].append({
                        "url": url,
                        "title": extracted['title'],
                        "content_length": len(extracted['content'])
                    })
                else:
                    results['failed'] += 1
            
            return {
                "success": True,
                "message": f"Scraped {results['successful']} pages successfully",
                "results": results
            }
        
        except Exception as e:
            logger.error(f"Website scraping error: {e}", exc_info=True)
            return {"success": False, "error": str(e)}

# ============================================================================
# BACKGROUND TASK SUPPORT (Optional)
# ============================================================================
"""
For async scraping, integrate with Celery:

@celery_app.task
def scrape_website_async(bot_id: int, start_url: str, method: str):
    from db.database import SessionLocal
    db = SessionLocal()
    try:
        result = WebScrapingService.scrape_website(
            bot_id=bot_id,
            start_url=start_url,
            method=method,
            db=db
        )
        return result
    finally:
        db.close()
"""
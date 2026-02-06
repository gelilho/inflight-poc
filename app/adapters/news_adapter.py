"""News Adapter - NewsAPI Integration"""

import requests
from typing import List, Dict
from config.settings import get_settings
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class NewsAdapter:
    """News adapter using NewsAPI.org"""
    
    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://newsapi.org/v2/everything"
        
        # City to country mapping for news search
        self.city_countries = {
            "Rome": "it",
            "London": "gb",
            "Paris": "fr"
        }
    
    def get_local_news(self, city: str, limit: int = 5) -> List[Dict]:
        """Get local news from NewsAPI"""
        
        # Check if we have API key
        if not self.settings.news_api_key or self.settings.use_mock_data:
            logger.warning("Using mock news data (no API key or mock mode enabled)")
            return self._get_mock_news(city, limit)
        
        try:
            # Get country code
            country = self.city_countries.get(city, "us")
            
            # Search for recent news about the city
            params = {
                "q": city,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": limit * 2,  # Get more to filter
                "apiKey": self.settings.news_api_key,
                "from": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Process and filter articles
            return self._process_api_news(data, limit)
        
        except Exception as e:
            logger.error(f"News API error: {e}, falling back to mock data")
            return self._get_mock_news(city, limit)
    
    def _process_api_news(self, data: dict, limit: int) -> List[Dict]:
        """Process NewsAPI response and filter for inflight safety"""
        
        # Keywords to exclude (violent, dramatic content)
        exclude_keywords = [
            "murder", "killed", "death", "terror", "attack", "shooting",
            "violence", "war", "crash", "disaster", "fire", "explosion"
        ]
        
        news_items = []
        articles = data.get("articles", [])
        
        for article in articles:
            if len(news_items) >= limit:
                break
            
            title = article.get("title", "")
            description = article.get("description", "")
            content = article.get("content", "")
            
            # Filter out dramatic content
            text_to_check = f"{title} {description}".lower()
            if any(keyword in text_to_check for keyword in exclude_keywords):
                continue
            
            # Categorize news
            category = self._categorize_news(title, description)
            
            news_items.append({
                "title": title[:100],  # Limit title length
                "brief_description": description[:150] if description else title[:150],
                "long_description": content[:500] if content else description[:500],
                "category": category
            })
        
        # If we don't have enough news, supplement with mock
        if len(news_items) < limit:
            logger.warning(f"Only found {len(news_items)} safe news items, using mock for rest")
            mock_news = self._get_mock_news("Generic", limit - len(news_items))
            news_items.extend(mock_news)
        
        return news_items[:limit]
    
    def _categorize_news(self, title: str, description: str) -> str:
        """Categorize news into allowed categories"""
        text = f"{title} {description}".lower()
        
        if any(word in text for word in ["football", "soccer", "sports", "team", "match", "player"]):
            return "sports"
        elif any(word in text for word in ["museum", "art", "culture", "festival", "music", "theater"]):
            return "culture"
        elif any(word in text for word in ["event", "celebration", "opening", "launch"]):
            return "events"
        else:
            return "local_interest"
    
    def _get_mock_news(self, city: str, limit: int = 5) -> List[Dict]:
        """Generate mock news (fallback)"""
        
        # Use Gemini to generate mock news (existing functionality)
        from app.adapters.gemini_adapter import gemini_adapter
        
        try:
            news_data = gemini_adapter.generate_mock_news(city)
            return news_data[:limit]
        except Exception as e:
            logger.error(f"Failed to generate mock news: {e}")
            return []


# Singleton instance
news_adapter = NewsAdapter()

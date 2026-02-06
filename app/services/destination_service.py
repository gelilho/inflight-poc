"""Destination Service - Handle destination content operations"""

from app.models.schemas import (
    DestinationContent, Destination, Highlight, Restaurant,
    AirportTransport, TransportOption, WeatherForecast, LocalNews,
    EmergencyContacts
)
from app.adapters.gemini_adapter import gemini_adapter
from app.adapters.weather_adapter import weather_adapter
from app.adapters.news_adapter import news_adapter
from data.loaders.csv_loader import csv_loader
from typing import List
import logging

logger = logging.getLogger(__name__)


class DestinationService:
    """Service for destination content operations"""
    
    def get_destination_content(self, airport_code: str, language: str = "en") -> DestinationContent:
        """Get complete destination content"""
        logger.info(f"Fetching destination content: {airport_code} in {language}")
        
        # Get destination info from CSV
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")
        
        destination = dest_info["destination"]
        emergency_contacts = dest_info["emergency_contacts"]
        
        # Generate content with Gemini
        highlights_data = gemini_adapter.generate_highlights(
            destination.city,
            destination.country
        )
        highlights = [Highlight(**h) for h in highlights_data]
        
        restaurants_data = gemini_adapter.generate_restaurants(
            destination.city,
            destination.country
        )
        restaurants = [Restaurant(**r) for r in restaurants_data]
        
        transport_data = gemini_adapter.generate_airport_transport(
            destination.city,
            airport_code
        )
        transport_options = [TransportOption(**t) for t in transport_data]
        airport_transport = AirportTransport(
            destination="main_train_station",
            options=transport_options
        )
        
        # Build content
        content = DestinationContent(
            destination=destination,
            highlights=highlights,
            emergency_contacts=emergency_contacts,
            restaurants=restaurants,
            airport_transport=airport_transport
        )
        
        # Translate if needed
        if language != "en":
            content = self._translate_content(content, language)
        
        return content
    
    def get_weather(self, airport_code: str, language: str = "en") -> List[WeatherForecast]:
        """Get weather forecast using real API"""
        logger.info(f"Fetching weather: {airport_code} in {language}")
        
        weather_data = weather_adapter.get_forecast(airport_code, days=3)
        forecasts = [WeatherForecast(**w) for w in weather_data]
        
        return forecasts
    
    def get_news(self, airport_code: str, language: str = "en") -> List[LocalNews]:
        """Get local news using real API or Gemini fallback"""
        logger.info(f"Fetching news: {airport_code} in {language}")
        
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")
        
        destination = dest_info["destination"]
        
        # Try real news API first
        news_data = news_adapter.get_local_news(destination.city, limit=5)
        news_items = [LocalNews(**n) for n in news_data]
        
        # Translate if needed
        if language != "en":
            for i, item in enumerate(news_items):
                try:
                    translated = gemini_adapter.translate_content(
                        item.model_dump(),
                        language
                    )
                    news_items[i] = LocalNews(**translated)
                except Exception as e:
                    logger.error(f"Failed to translate news item: {e}")
        
        return news_items
    
    def _translate_content(self, content: DestinationContent, language: str) -> DestinationContent:
        """Translate content"""
        try:
            content_dict = content.model_dump()
            translated = gemini_adapter.translate_content(content_dict, language)
            return DestinationContent(**translated)
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return content


# Singleton instance
destination_service = DestinationService()

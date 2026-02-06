"""Destination Service - Handle destination content operations"""

from app.models.schemas import (
    DestinationContent, Destination, Highlight, Restaurant,
    AirportTransport, TransportOption, WeatherForecast, LocalNews,
    EmergencyContacts
)
from app.adapters.gemini_adapter import gemini_adapter
from app.adapters.weather_adapter import weather_adapter
from data.loaders.csv_loader import csv_loader
from typing import List
import logging

logger = logging.getLogger(__name__)


class DestinationService:
    """Service for destination content operations"""
    
    def get_destination_content(self, airport_code: str, language: str = "en") -> DestinationContent:
        """
        Get complete destination content (highlights, restaurants, transport, emergency)
        """
        logger.info(f"Fetching destination content: {airport_code} in {language}")
        
        # Get destination info and emergency contacts from CSV
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")
        
        destination = dest_info["destination"]
        emergency_contacts = dest_info["emergency_contacts"]
        
        # Generate highlights (base language)
        highlights_data = gemini_adapter.generate_highlights(
            destination.city,
            destination.country
        )
        highlights = [Highlight(**h) for h in highlights_data]
        
        # Generate restaurants (base language)
        restaurants_data = gemini_adapter.generate_restaurants(
            destination.city,
            destination.country
        )
        restaurants = [Restaurant(**r) for r in restaurants_data]
        
        # Generate transport options (base language)
        transport_data = gemini_adapter.generate_airport_transport(
            destination.city,
            airport_code
        )
        transport_options = [TransportOption(**t) for t in transport_data]
        airport_transport = AirportTransport(
            destination="main_train_station",
            options=transport_options
        )
        
        # Build destination content
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
        """Get 3-day weather forecast"""
        logger.info(f"Fetching weather: {airport_code} in {language}")
        
        weather_data = weather_adapter.get_forecast(airport_code, days=3)
        forecasts = [WeatherForecast(**w) for w in weather_data]
        
        # TODO: Translate weather conditions if needed
        
        return forecasts
    
    def get_news(self, airport_code: str, language: str = "en") -> List[LocalNews]:
        """Get local news headlines"""
        logger.info(f"Fetching news: {airport_code} in {language}")
        
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")
        
        destination = dest_info["destination"]
        news_data = gemini_adapter.generate_mock_news(destination.city)
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
        """Translate destination content to target language"""
        try:
            content_dict = content.model_dump()
            translated = gemini_adapter.translate_content(content_dict, language)
            return DestinationContent(**translated)
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return content  # Fallback to base language


# Singleton instance
destination_service = DestinationService()

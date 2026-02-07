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
        
        # Generate content with Gemini (with fallback to static defaults)
        try:
            highlights_data = gemini_adapter.generate_highlights(
                destination.city,
                destination.country
            )
            highlights = [Highlight(**h) for h in highlights_data]
        except Exception as e:
            logger.error(f"Gemini highlights failed: {e}, using fallback")
            highlights = self._fallback_highlights(destination.city)

        try:
            restaurants_data = gemini_adapter.generate_restaurants(
                destination.city,
                destination.country
            )
            restaurants = [Restaurant(**r) for r in restaurants_data]
        except Exception as e:
            logger.error(f"Gemini restaurants failed: {e}, using fallback")
            restaurants = self._fallback_restaurants(destination.city)

        try:
            transport_data = gemini_adapter.generate_airport_transport(
                destination.city,
                airport_code
            )
            transport_options = [TransportOption(**t) for t in transport_data]
            airport_transport = AirportTransport(
                destination="main_train_station",
                options=transport_options
            )
        except Exception as e:
            logger.error(f"Gemini transport failed: {e}, using fallback")
            airport_transport = self._fallback_transport()
        
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
    
    # ------------------------------------------------------------------
    # Fallbacks — static defaults when Gemini is unreachable
    # ------------------------------------------------------------------

    @staticmethod
    def _fallback_highlights(city: str) -> List[Highlight]:
        """Return 5 generic highlights when AI generation fails"""
        return [
            Highlight(
                id=f"H00{i}",
                title=f"{city} Highlight {i}",
                brief_description=f"Discover a must-see spot in {city}.",
                long_description=f"This is one of the most popular places to visit in {city}. "
                                 "Ask your cabin crew or check the local tourism office for details."
            )
            for i in range(1, 6)
        ]

    @staticmethod
    def _fallback_restaurants(city: str) -> List[Restaurant]:
        """Return 3 generic restaurants when AI generation fails"""
        cuisines = ["Local", "Mediterranean", "International"]
        return [
            Restaurant(
                name=f"{city} Restaurant {i}",
                cuisine=cuisines[i - 1],
                brief_description=f"A popular {cuisines[i - 1].lower()} restaurant in {city}.",
                long_description=f"Enjoy authentic {cuisines[i - 1].lower()} cuisine in the heart of {city}. "
                                 "Check local reviews for the latest recommendations."
            )
            for i in range(1, 4)
        ]

    @staticmethod
    def _fallback_transport() -> AirportTransport:
        """Return a safe default transport option when AI generation fails"""
        return AirportTransport(
            destination="main_train_station",
            options=[
                TransportOption(mode="taxi", estimated_duration_minutes=30, notes="Available at arrivals exit")
            ]
        )

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

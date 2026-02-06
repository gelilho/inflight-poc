"""FLOW A: Destination Experience Content Service"""

from app.models.schemas import (
    DestinationExperience, Destination, Highlight, Restaurant,
    AirportTransport, TransportOption, WeatherForecast, LocalNews,
    Translations, TranslatedDestinationExperience,
    DestinationExperienceWithTranslations
)
from app.adapters.gemini_adapter import gemini_adapter
from app.adapters.weather_adapter import weather_adapter
from data.loaders.csv_loader import csv_loader
from config.constants import SUPPORTED_LANGUAGES
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)


class FlowAService:
    """Service for generating destination experience content"""
    
    def generate_destination_content_base(self, airport_code: str) -> DestinationExperience:
        """
        Generate base destination content (WITHOUT weather and news)
        
        This includes:
        - Destination info
        - Emergency numbers
        - Highlights
        - Restaurants
        - Airport transport
        - Weather (placeholder/empty for now - fetched separately)
        - News (placeholder/empty for now - fetched separately)
        """
        
        logger.info(f"Generating destination content for: {airport_code}")
        
        # Get destination info from CSV
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found for airport code: {airport_code}")
        
        destination = dest_info["destination"]
        emergency_numbers = dest_info["emergency_numbers"]
        
        logger.info(f"Destination: {destination.city}, {destination.country}")
        
        # Generate highlights
        highlights_data = gemini_adapter.generate_highlights(
            destination.city, 
            destination.country
        )
        highlights = [Highlight(**h) for h in highlights_data]
        
        # Generate restaurants
        restaurants_data = gemini_adapter.generate_restaurants(
            destination.city,
            destination.country
        )
        restaurants = [Restaurant(**r) for r in restaurants_data]
        
        # Generate airport transport
        transport_data = gemini_adapter.generate_airport_transport(
            destination.city,
            airport_code
        )
        transport_options = [TransportOption(**t) for t in transport_data]
        airport_transport = AirportTransport(
            destination="main_train_station",
            options=transport_options
        )
        
        # Get weather and news separately (using dedicated methods)
        weather_forecast = self.get_weather(airport_code, "en")
        local_news = self.get_news(airport_code, "en")
        
        # Build complete destination experience
        experience = DestinationExperience(
            destination=destination,
            highlights=highlights,
            emergency_numbers=emergency_numbers,
            restaurants=restaurants,
            airport_transport=airport_transport,
            weather_forecast=weather_forecast,
            local_news=local_news
        )
        
        logger.info("Destination content generated successfully")
        return experience
    
    def translate_single_language(
        self,
        experience: DestinationExperience,
        target_language: str
    ) -> DestinationExperience:
        """Translate destination experience to a single language"""
        
        logger.info(f"Translating to {target_language}...")
        
        experience_dict = experience.model_dump()
        
        try:
            translated = gemini_adapter.translate_content(
                experience_dict,
                target_language
            )
            return DestinationExperience(**translated)
        
        except Exception as e:
            logger.error(f"Translation to {target_language} failed: {e}")
            return experience  # Fallback to base language
    
    def get_weather(self, airport_code: str, language: str) -> List[WeatherForecast]:
        """Get weather forecast (with optional translation)"""
        
        logger.info(f"Fetching weather for {airport_code} in {language}")
        weather_data = weather_adapter.get_forecast(airport_code, days=3)
        forecasts = [WeatherForecast(**w) for w in weather_data]
        
        # In production, translate weather condition strings
        # For now, return as-is
        
        return forecasts
    
    def get_news(self, airport_code: str, language: str) -> List[LocalNews]:
        """Get local news (with optional translation)"""
        
        logger.info(f"Fetching news for {airport_code} in {language}")
        
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")
        
        destination = dest_info["destination"]
        news_data = gemini_adapter.generate_mock_news(destination.city)
        news_items = [LocalNews(**n) for n in news_data]
        
        # If not English, translate news
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


# Singleton instance
flow_a_service = FlowAService()

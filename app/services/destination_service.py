"""
Destination Service — speed-optimised.

Key change: Gemini generates content directly in the target language.
This eliminates the expensive translation step (was adding ~15-20s).
"""

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
        """Get complete destination content — generated directly in target language"""
        logger.info(f"Fetching destination content: {airport_code} in {language}")

        # Get destination info from CSV
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")

        destination = dest_info["destination"]
        emergency_contacts = dest_info["emergency_contacts"]

        # Generate content with Gemini DIRECTLY in the target language
        try:
            highlights_data = gemini_adapter.generate_highlights(
                destination.city, destination.country, language
            )
            highlights = [Highlight(**h) for h in highlights_data]
        except Exception as e:
            logger.error(f"Gemini highlights failed: {e}, using fallback")
            highlights = self._fallback_highlights(destination.city)

        try:
            restaurants_data = gemini_adapter.generate_restaurants(
                destination.city, destination.country, language
            )
            restaurants = [Restaurant(**r) for r in restaurants_data]
        except Exception as e:
            logger.error(f"Gemini restaurants failed: {e}, using fallback")
            restaurants = self._fallback_restaurants(destination.city)

        try:
            transport_data = gemini_adapter.generate_airport_transport(
                destination.city, airport_code, language
            )
            transport_options = [TransportOption(**t) for t in transport_data]
            airport_transport = AirportTransport(
                destination="main_train_station",
                options=transport_options
            )
        except Exception as e:
            logger.error(f"Gemini transport failed: {e}, using fallback")
            airport_transport = self._fallback_transport()

        # Build content — NO translation step needed!
        content = DestinationContent(
            destination=destination,
            highlights=highlights,
            emergency_contacts=emergency_contacts,
            restaurants=restaurants,
            airport_transport=airport_transport
        )

        return content

    def get_weather(self, airport_code: str, language: str = "en") -> List[WeatherForecast]:
        """Get weather forecast using real API"""
        logger.info(f"Fetching weather: {airport_code} in {language}")

        weather_data = weather_adapter.get_forecast(airport_code, days=3)
        forecasts = [WeatherForecast(**w) for w in weather_data]

        return forecasts

    def get_news(self, airport_code: str, language: str = "en") -> List[LocalNews]:
        """Get local news — Gemini generates directly in the target language"""
        logger.info(f"Fetching news: {airport_code} in {language}")

        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")

        destination = dest_info["destination"]

        # Try real news API first (English results)
        try:
            news_data = news_adapter.get_local_news(destination.city, limit=5)
            if news_data and len(news_data) >= 3:
                news_items = [LocalNews(**n) for n in news_data]
                # Translate if needed (news API returns English)
                if language != "en":
                    for i, item in enumerate(news_items):
                        try:
                            translated = gemini_adapter.translate_content(
                                item.model_dump(), language
                            )
                            news_items[i] = LocalNews(**translated)
                        except Exception as e:
                            logger.error(f"Failed to translate news item: {e}")
                return news_items
        except Exception as e:
            logger.warning(f"News API failed: {e}, falling back to Gemini")

        # Fallback: generate news directly in the target language with Gemini
        try:
            news_data = gemini_adapter.generate_mock_news(destination.city, language)
            return [LocalNews(**n) for n in news_data]
        except Exception as e:
            logger.error(f"Gemini news also failed: {e}")
            return []

    # ------------------------------------------------------------------
    # Fallbacks — static defaults when Gemini is unreachable
    # ------------------------------------------------------------------

    @staticmethod
    def _fallback_highlights(city: str) -> List[Highlight]:
        return [
            Highlight(
                id=f"H00{i}",
                title=f"{city} Highlight {i}",
                brief_description=f"Discover a must-see spot in {city}.",
                long_description=f"One of the most popular places to visit in {city}. "
                                 "Ask your cabin crew for details."
            )
            for i in range(1, 6)
        ]

    @staticmethod
    def _fallback_restaurants(city: str) -> List[Restaurant]:
        cuisines = ["Local", "Mediterranean", "International"]
        return [
            Restaurant(
                name=f"{city} Restaurant {i}",
                cuisine=cuisines[i - 1],
                brief_description=f"Popular {cuisines[i - 1].lower()} restaurant in {city}.",
                long_description=f"Enjoy authentic {cuisines[i - 1].lower()} cuisine in {city}."
            )
            for i in range(1, 4)
        ]

    @staticmethod
    def _fallback_transport() -> AirportTransport:
        return AirportTransport(
            destination="main_train_station",
            options=[
                TransportOption(mode="taxi", estimated_duration_minutes=30, notes="Available at arrivals exit")
            ]
        )


# Singleton instance
destination_service = DestinationService()

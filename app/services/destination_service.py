"""
Destination Service — with in-memory cache and startup pre-warming.

Architecture:
- In-memory cache keyed by (airport_code, language) for content, weather, news
- On API startup, pre-warms cache for configured destinations + languages
- First UI request hits cache → <50ms response instead of 20-30s
- Cache lives for the lifetime of the process (fine for a PoC/demo)
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
from typing import List, Dict, Tuple, Optional
import logging
import time

logger = logging.getLogger(__name__)


class DestinationService:
    """Service for destination content with in-memory caching"""

    def __init__(self):
        # Cache: (airport_code, language) → response
        self._content_cache: Dict[Tuple[str, str], DestinationContent] = {}
        self._weather_cache: Dict[Tuple[str, str], List[WeatherForecast]] = {}
        self._news_cache: Dict[Tuple[str, str], List[LocalNews]] = {}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def get_destination_content(self, airport_code: str, language: str = "en") -> DestinationContent:
        """Get destination content — from cache if available, else generate"""
        cache_key = (airport_code, language)

        if cache_key in self._content_cache:
            logger.info(f"CACHE HIT: destination content {airport_code}/{language}")
            return self._content_cache[cache_key]

        logger.info(f"CACHE MISS: generating destination content {airport_code}/{language}")
        start = time.perf_counter()

        content = self._generate_content(airport_code, language)
        self._content_cache[cache_key] = content

        elapsed = round((time.perf_counter() - start) * 1000)
        logger.info(f"Destination content generated in {elapsed}ms — cached for next request")

        return content

    def get_weather(self, airport_code: str, language: str = "en") -> List[WeatherForecast]:
        """Get weather — from cache if available"""
        cache_key = (airport_code, language)

        if cache_key in self._weather_cache:
            logger.info(f"CACHE HIT: weather {airport_code}/{language}")
            return self._weather_cache[cache_key]

        logger.info(f"CACHE MISS: fetching weather {airport_code}/{language}")
        start = time.perf_counter()

        weather_data = weather_adapter.get_forecast(airport_code, days=3)
        forecasts = [WeatherForecast(**w) for w in weather_data]
        self._weather_cache[cache_key] = forecasts

        elapsed = round((time.perf_counter() - start) * 1000)
        logger.info(f"Weather fetched in {elapsed}ms — cached")

        return forecasts

    def get_news(self, airport_code: str, language: str = "en") -> List[LocalNews]:
        """Get news — from cache if available"""
        cache_key = (airport_code, language)

        if cache_key in self._news_cache:
            logger.info(f"CACHE HIT: news {airport_code}/{language}")
            return self._news_cache[cache_key]

        logger.info(f"CACHE MISS: fetching news {airport_code}/{language}")
        start = time.perf_counter()

        news_items = self._fetch_news(airport_code, language)
        self._news_cache[cache_key] = news_items

        elapsed = round((time.perf_counter() - start) * 1000)
        logger.info(f"News fetched in {elapsed}ms — cached")

        return news_items

    # ------------------------------------------------------------------
    # Pre-warming (called from app startup)
    # ------------------------------------------------------------------

    def prewarm(self, airports: List[str], languages: List[str]):
        """Pre-generate and cache content for given airport+language combos.

        Called on API startup so the first UI request is instant.
        """
        total = len(airports) * len(languages)
        logger.info(f"🔥 PRE-WARMING CACHE: {len(airports)} airports × {len(languages)} languages = {total} combos")
        overall_start = time.perf_counter()

        for airport_code in airports:
            for language in languages:
                tag = f"{airport_code}/{language}"
                try:
                    start = time.perf_counter()
                    self.get_destination_content(airport_code, language)
                    elapsed = round((time.perf_counter() - start) * 1000)
                    logger.info(f"  ✅ {tag} content ready ({elapsed}ms)")
                except Exception as e:
                    logger.error(f"  ❌ {tag} content failed: {e}")

                try:
                    self.get_weather(airport_code, language)
                    logger.info(f"  ✅ {tag} weather ready")
                except Exception as e:
                    logger.error(f"  ❌ {tag} weather failed: {e}")

                try:
                    self.get_news(airport_code, language)
                    logger.info(f"  ✅ {tag} news ready")
                except Exception as e:
                    logger.error(f"  ❌ {tag} news failed: {e}")

        total_elapsed = round((time.perf_counter() - overall_start) * 1000)
        cached = len(self._content_cache)
        logger.info(f"🔥 PRE-WARM COMPLETE: {cached} destinations cached in {total_elapsed/1000:.1f}s")

    # ------------------------------------------------------------------
    # Internal — content generation
    # ------------------------------------------------------------------

    def _generate_content(self, airport_code: str, language: str) -> DestinationContent:
        """Generate content with Gemini directly in the target language"""
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")

        destination = dest_info["destination"]
        emergency_contacts = dest_info["emergency_contacts"]

        # Generate each piece with Gemini (with fallback)
        try:
            start = time.perf_counter()
            highlights_data = gemini_adapter.generate_highlights(
                destination.city, destination.country, language
            )
            highlights = [Highlight(**h) for h in highlights_data]
            logger.info(f"  Highlights: {round((time.perf_counter()-start)*1000)}ms")
        except Exception as e:
            logger.error(f"Gemini highlights failed: {e}, using fallback")
            highlights = self._fallback_highlights(destination.city)

        try:
            start = time.perf_counter()
            restaurants_data = gemini_adapter.generate_restaurants(
                destination.city, destination.country, language
            )
            restaurants = [Restaurant(**r) for r in restaurants_data]
            logger.info(f"  Restaurants: {round((time.perf_counter()-start)*1000)}ms")
        except Exception as e:
            logger.error(f"Gemini restaurants failed: {e}, using fallback")
            restaurants = self._fallback_restaurants(destination.city)

        try:
            start = time.perf_counter()
            transport_data = gemini_adapter.generate_airport_transport(
                destination.city, airport_code, language
            )
            transport_options = [TransportOption(**t) for t in transport_data]
            airport_transport = AirportTransport(
                destination="main_train_station",
                options=transport_options
            )
            logger.info(f"  Transport: {round((time.perf_counter()-start)*1000)}ms")
        except Exception as e:
            logger.error(f"Gemini transport failed: {e}, using fallback")
            airport_transport = self._fallback_transport()

        return DestinationContent(
            destination=destination,
            highlights=highlights,
            emergency_contacts=emergency_contacts,
            restaurants=restaurants,
            airport_transport=airport_transport
        )

    def _fetch_news(self, airport_code: str, language: str) -> List[LocalNews]:
        """Fetch news from API or generate with Gemini"""
        dest_info = csv_loader.get_destination_info(airport_code)
        if not dest_info:
            raise ValueError(f"Destination not found: {airport_code}")

        destination = dest_info["destination"]

        # Try real news API first
        try:
            news_data = news_adapter.get_local_news(destination.city, limit=5)
            if news_data and len(news_data) >= 3:
                news_items = [LocalNews(**n) for n in news_data]
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

        # Fallback: Gemini generates directly in the target language
        try:
            news_data = gemini_adapter.generate_mock_news(destination.city, language)
            return [LocalNews(**n) for n in news_data]
        except Exception as e:
            logger.error(f"Gemini news also failed: {e}")
            return []

    # ------------------------------------------------------------------
    # Fallbacks
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

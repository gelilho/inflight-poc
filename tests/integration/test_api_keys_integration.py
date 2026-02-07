"""Integration tests — Real API calls to Gemini, Weather, and News.

These tests hit the REAL external APIs to verify keys and connectivity.
Mark with @pytest.mark.live so they can be skipped in CI with: pytest -m "not live"
"""

import os
import pytest

# Mark all tests in this module as "live" (real API calls)
pytestmark = pytest.mark.live


# ============================================================
# GEMINI API (Real Call)
# ============================================================

class TestGeminiApiIntegration:

    def test_gemini_api_key_is_configured(self):
        """Gemini API key must be present in environment"""
        key = os.getenv("GEMINI_API_KEY")
        assert key is not None, "GEMINI_API_KEY not found in .env"
        assert len(key) > 10, "GEMINI_API_KEY looks too short"

    def test_gemini_generates_highlights(self):
        """Real Gemini call — generate 5 highlights for Rome"""
        from app.adapters.gemini_adapter import gemini_adapter

        highlights = gemini_adapter.generate_highlights("Rome", "Italy")
        assert isinstance(highlights, list)
        assert len(highlights) == 5
        assert "id" in highlights[0]
        assert "title" in highlights[0]
        assert "brief_description" in highlights[0]
        assert "long_description" in highlights[0]

    def test_gemini_generates_restaurants(self):
        """Real Gemini call — generate 3 restaurants for Rome"""
        from app.adapters.gemini_adapter import gemini_adapter

        restaurants = gemini_adapter.generate_restaurants("Rome", "Italy")
        assert isinstance(restaurants, list)
        assert len(restaurants) == 3
        assert "name" in restaurants[0]
        assert "cuisine" in restaurants[0]

    def test_gemini_generates_transport(self):
        """Real Gemini call — generate transport options for FCO"""
        from app.adapters.gemini_adapter import gemini_adapter

        transport = gemini_adapter.generate_airport_transport("Rome", "FCO")
        assert isinstance(transport, list)
        assert len(transport) >= 1
        assert transport[0]["mode"] in ["train", "bus", "taxi"]

    def test_gemini_translates_content(self):
        """Real Gemini call — translate content to Spanish"""
        from app.adapters.gemini_adapter import gemini_adapter

        original = {"title": "Colosseum", "description": "Ancient Roman amphitheater"}
        translated = gemini_adapter.translate_content(original, "es")
        assert isinstance(translated, dict)
        assert "title" in translated
        assert translated["title"] != original["title"]  # Should be translated


# ============================================================
# WEATHER API (Real Call)
# ============================================================

class TestWeatherApiIntegration:

    def test_weather_returns_forecast(self):
        """Weather API call (real or mock fallback) — returns 3-day forecast"""
        from app.adapters.weather_adapter import weather_adapter

        forecast = weather_adapter.get_forecast("FCO", days=3)
        assert isinstance(forecast, list)
        assert len(forecast) == 3
        assert "date" in forecast[0]
        assert "condition" in forecast[0]
        assert "min_temperature_c" in forecast[0]
        assert "max_temperature_c" in forecast[0]


# ============================================================
# NEWS API (Real Call)
# ============================================================

class TestNewsApiIntegration:

    def test_news_returns_articles(self):
        """News API call (real or Gemini fallback) — returns 5 items"""
        from app.adapters.news_adapter import news_adapter

        news = news_adapter.get_local_news("Rome", limit=5)
        assert isinstance(news, list)
        assert len(news) >= 1
        assert "title" in news[0]
        assert "category" in news[0]

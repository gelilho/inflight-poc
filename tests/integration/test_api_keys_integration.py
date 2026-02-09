"""Integration tests — Real API calls to Gemini, Weather, and News.

These tests hit the REAL external APIs to verify keys and connectivity.
Mark with @pytest.mark.live so they can be skipped in CI with: pytest -m "not live"

Each Gemini call is timed so we can track latency improvements.
"""

import pytest
import time
from config.settings import get_settings

# Mark all tests in this module as "live" (real API calls)
pytestmark = pytest.mark.live


def _timed(label: str):
    """Context manager that prints timing for a block"""
    class Timer:
        def __init__(self):
            self.elapsed_ms = 0
        def __enter__(self):
            self.start = time.perf_counter()
            return self
        def __exit__(self, *args):
            self.elapsed_ms = round((time.perf_counter() - self.start) * 1000)
            print(f"\n  ⏱  {label}: {self.elapsed_ms}ms ({self.elapsed_ms/1000:.1f}s)")
    return Timer()


# ============================================================
# GEMINI API (Real Call)
# ============================================================

class TestGeminiApiIntegration:

    def test_gemini_api_key_is_configured(self):
        """Gemini API key must be present in settings"""
        settings = get_settings()
        assert settings.gemini_api_key is not None, "GEMINI_API_KEY not configured"
        assert len(settings.gemini_api_key) > 10, "GEMINI_API_KEY looks too short"

    def test_gemini_generates_highlights(self):
        """Real Gemini call — generate 5 highlights for Rome"""
        from app.adapters.gemini_adapter import gemini_adapter

        with _timed("Gemini highlights (Rome, en)") as t:
            highlights = gemini_adapter.generate_highlights("Rome", "Italy")

        assert isinstance(highlights, list)
        assert len(highlights) == 5
        assert "id" in highlights[0]
        assert "title" in highlights[0]
        assert "brief_description" in highlights[0]
        assert "long_description" in highlights[0]
        assert t.elapsed_ms < 60_000, f"Highlights took too long: {t.elapsed_ms}ms"

    def test_gemini_generates_highlights_spanish(self):
        """Real Gemini call — generate 5 highlights in Spanish (direct, no translation)"""
        from app.adapters.gemini_adapter import gemini_adapter

        with _timed("Gemini highlights (Rome, es)") as t:
            highlights = gemini_adapter.generate_highlights("Rome", "Italy", "es")

        assert isinstance(highlights, list)
        assert len(highlights) == 5
        assert t.elapsed_ms < 60_000, f"Highlights (es) took too long: {t.elapsed_ms}ms"

    def test_gemini_generates_restaurants(self):
        """Real Gemini call — generate 3 restaurants for Rome"""
        from app.adapters.gemini_adapter import gemini_adapter

        with _timed("Gemini restaurants (Rome, en)") as t:
            restaurants = gemini_adapter.generate_restaurants("Rome", "Italy")

        assert isinstance(restaurants, list)
        assert len(restaurants) == 3
        assert "name" in restaurants[0]
        assert "cuisine" in restaurants[0]
        assert t.elapsed_ms < 60_000, f"Restaurants took too long: {t.elapsed_ms}ms"

    def test_gemini_generates_transport(self):
        """Real Gemini call — generate transport options for FCO"""
        from app.adapters.gemini_adapter import gemini_adapter

        with _timed("Gemini transport (FCO)") as t:
            transport = gemini_adapter.generate_airport_transport("Rome", "FCO")

        assert isinstance(transport, list)
        assert len(transport) >= 1
        assert transport[0]["mode"] in ["train", "bus", "taxi"]
        assert t.elapsed_ms < 30_000, f"Transport took too long: {t.elapsed_ms}ms"

    def test_gemini_translates_content(self):
        """Real Gemini call — translate content to Spanish"""
        from app.adapters.gemini_adapter import gemini_adapter

        original = {"title": "The Roman Forum", "description": "Ancient Roman marketplace and civic centre"}

        with _timed("Gemini translate (en→es)") as t:
            translated = gemini_adapter.translate_content(original, "es")

        assert isinstance(translated, dict)
        assert "title" in translated
        # At least one field must differ (Gemini should translate)
        assert (
            translated["title"] != original["title"]
            or translated.get("description", "") != original["description"]
        ), "Nothing was translated — Gemini returned the original text"
        assert t.elapsed_ms < 30_000, f"Translation took too long: {t.elapsed_ms}ms"

    def test_gemini_generates_news(self):
        """Real Gemini call — generate 5 news items for Rome in Spanish"""
        from app.adapters.gemini_adapter import gemini_adapter

        with _timed("Gemini news (Rome, es)") as t:
            news = gemini_adapter.generate_mock_news("Rome", "es")

        assert isinstance(news, list)
        assert len(news) == 5
        assert "title" in news[0]
        assert "category" in news[0]
        assert t.elapsed_ms < 60_000, f"News took too long: {t.elapsed_ms}ms"


# ============================================================
# WEATHER API (Real Call)
# ============================================================

class TestWeatherApiIntegration:

    def test_weather_returns_forecast(self):
        """Weather API call (real or mock fallback) — returns 3-day forecast"""
        from app.adapters.weather_adapter import weather_adapter

        with _timed("Weather forecast (FCO)") as t:
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

        with _timed("News API (Rome)") as t:
            news = news_adapter.get_local_news("Rome", limit=5)

        assert isinstance(news, list)
        assert len(news) >= 1
        assert "title" in news[0]
        assert "category" in news[0]

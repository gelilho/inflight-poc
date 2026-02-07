"""Unit tests for news content filtering and categorization — inflight safety"""

import pytest
from unittest.mock import patch
from app.adapters.news_adapter import NewsAdapter


@pytest.fixture
def adapter():
    """NewsAdapter instance (no real API calls in these tests)"""
    return NewsAdapter()


# ============================================================
# NEWS CATEGORIZATION
# ============================================================

class TestNewsCategorization:

    def test_sports_keywords(self, adapter):
        assert adapter._categorize_news("Roma wins football match", "") == "sports"
        assert adapter._categorize_news("", "soccer team advances") == "sports"
        assert adapter._categorize_news("Player transfer confirmed", "") == "sports"

    def test_culture_keywords(self, adapter):
        assert adapter._categorize_news("New museum exhibition opens", "") == "culture"
        assert adapter._categorize_news("", "art festival this weekend") == "culture"
        assert adapter._categorize_news("Theater season announced", "") == "culture"
        assert adapter._categorize_news("Music concert at the park", "") == "culture"

    def test_events_keywords(self, adapter):
        assert adapter._categorize_news("Grand opening celebration", "") == "events"
        assert adapter._categorize_news("", "new venue launch today") == "events"

    def test_defaults_to_local_interest(self, adapter):
        assert adapter._categorize_news("Mayor announces new park", "") == "local_interest"
        assert adapter._categorize_news("Traffic improvements coming", "") == "local_interest"


# ============================================================
# NEWS CONTENT FILTERING (Inflight Safety)
# ============================================================

class TestNewsContentFiltering:
    """Test that violent/dramatic content is filtered out.

    We mock _get_mock_news to avoid hitting Gemini when filtered results
    are fewer than the requested limit.
    """

    def _make_api_response(self, articles):
        """Build a fake NewsAPI response"""
        return {
            "status": "ok",
            "articles": [
                {
                    "title": a.get("title", ""),
                    "description": a.get("description", ""),
                    "content": a.get("content", "")
                }
                for a in articles
            ]
        }

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_safe_articles_pass_through(self, mock_fallback, adapter):
        data = self._make_api_response([
            {"title": "Roma wins 2-1", "description": "Great match"},
            {"title": "New art exhibition", "description": "Modern art show"},
        ])
        result = adapter._process_api_news(data, limit=2)
        assert len(result) == 2

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_violent_title_filtered_out(self, mock_fallback, adapter):
        data = self._make_api_response([
            {"title": "Man killed in accident", "description": "Tragic event"},
            {"title": "Museum opens new wing", "description": "Culture news"},
        ])
        result = adapter._process_api_news(data, limit=5)
        safe_titles = [item["title"] for item in result]
        assert "Man killed in accident" not in safe_titles

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_terror_keyword_filtered(self, mock_fallback, adapter):
        data = self._make_api_response([
            {"title": "Terror alert in city center", "description": "Security concern"},
        ])
        result = adapter._process_api_news(data, limit=5)
        safe_titles = [item["title"] for item in result]
        assert "Terror alert in city center" not in safe_titles

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_violence_in_description_filtered(self, mock_fallback, adapter):
        data = self._make_api_response([
            {"title": "Breaking news", "description": "Violence erupts at protest"},
        ])
        result = adapter._process_api_news(data, limit=5)
        safe_titles = [item["title"] for item in result]
        assert "Breaking news" not in safe_titles

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_all_excluded_keywords_are_filtered(self, mock_fallback, adapter):
        """Every single excluded keyword must cause filtering"""
        excluded = [
            "murder", "killed", "death", "terror", "attack", "shooting",
            "violence", "war", "crash", "disaster", "fire", "explosion"
        ]
        for keyword in excluded:
            data = self._make_api_response([
                {"title": f"Story about {keyword}", "description": "Details"},
            ])
            result = adapter._process_api_news(data, limit=5)
            safe_titles = [item["title"] for item in result]
            assert f"Story about {keyword}" not in safe_titles, \
                f"Keyword '{keyword}' should be filtered but wasn't"

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_limit_respected(self, mock_fallback, adapter):
        data = self._make_api_response([
            {"title": f"Good news {i}", "description": "Positive story"}
            for i in range(10)
        ])
        result = adapter._process_api_news(data, limit=5)
        assert len(result) <= 5

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_title_truncated_to_100_chars(self, mock_fallback, adapter):
        long_title = "A" * 200
        data = self._make_api_response([
            {"title": long_title, "description": "Brief"},
        ])
        result = adapter._process_api_news(data, limit=1)
        assert len(result[0]["title"]) <= 100

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_categorization_applied_to_results(self, mock_fallback, adapter):
        data = self._make_api_response([
            {"title": "Football team wins trophy", "description": "Sports news"},
        ])
        result = adapter._process_api_news(data, limit=1)
        assert result[0]["category"] == "sports"

    @patch.object(NewsAdapter, "_get_mock_news", return_value=[])
    def test_fallback_called_when_not_enough_safe_articles(self, mock_fallback, adapter):
        """When all articles are filtered, fallback is triggered"""
        data = self._make_api_response([
            {"title": "Explosion rocks city", "description": "Disaster strikes"},
        ])
        adapter._process_api_news(data, limit=5)
        mock_fallback.assert_called_once()

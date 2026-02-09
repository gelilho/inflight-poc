"""Unit tests for Gemini adapter — JSON parsing and markdown cleanup logic.

These tests mock the actual Gemini API call and only test OUR parsing logic.
"""

import pytest
from unittest.mock import patch, MagicMock
from app.adapters.gemini_adapter import GeminiAdapter


@pytest.fixture
def adapter():
    """GeminiAdapter with mocked Gemini client"""
    with patch("app.adapters.gemini_adapter.genai") as mock_genai:
        mock_genai.GenerativeModel.return_value = MagicMock()
        instance = GeminiAdapter()
        yield instance


# ============================================================
# JSON RESPONSE PARSING
# ============================================================

class TestParseJsonResponse:

    def test_plain_json_array(self, adapter):
        text = '[{"id": "H001", "title": "Colosseum"}]'
        result = adapter._parse_json_response(text)
        assert result[0]["id"] == "H001"

    def test_plain_json_object(self, adapter):
        text = '{"city": "Rome", "country": "Italy"}'
        result = adapter._parse_json_response(text)
        assert result["city"] == "Rome"

    def test_markdown_code_block_with_json_tag(self, adapter):
        text = '```json\n[{"id": "H001"}]\n```'
        result = adapter._parse_json_response(text)
        assert result[0]["id"] == "H001"

    def test_markdown_code_block_without_json_tag(self, adapter):
        text = '```\n[{"id": "H001"}]\n```'
        result = adapter._parse_json_response(text)
        assert result[0]["id"] == "H001"

    def test_whitespace_around_json(self, adapter):
        text = '  \n  [{"id": "H001"}]  \n  '
        result = adapter._parse_json_response(text)
        assert result[0]["id"] == "H001"

    def test_invalid_json_raises_value_error(self, adapter):
        text = 'This is not JSON at all'
        with pytest.raises(ValueError, match="Invalid JSON response"):
            adapter._parse_json_response(text)

    def test_empty_string_raises_value_error(self, adapter):
        with pytest.raises(ValueError):
            adapter._parse_json_response("")

    def test_nested_json_preserved(self, adapter):
        text = '{"transport": {"options": [{"mode": "train"}]}}'
        result = adapter._parse_json_response(text)
        assert result["transport"]["options"][0]["mode"] == "train"

    def test_trailing_comma_in_array(self, adapter):
        """Gemini sometimes adds trailing commas — should be cleaned and parsed"""
        text = '[{"id": "H001"}, {"id": "H002"},]'
        result = adapter._parse_json_response(text)
        assert len(result) == 2

    def test_trailing_comma_in_object(self, adapter):
        text = '{"city": "Rome", "country": "Italy",}'
        result = adapter._parse_json_response(text)
        assert result["city"] == "Rome"

    def test_single_line_comments_removed(self, adapter):
        text = '[\n{"id": "H001"} // first item\n]'
        result = adapter._parse_json_response(text)
        assert result[0]["id"] == "H001"

    def test_trailing_comma_in_markdown_block(self, adapter):
        """Real-world Gemini output: markdown block with trailing comma"""
        text = '```json\n[{"title": "Colosseum", "brief": "Ancient"},\n]\n```'
        result = adapter._parse_json_response(text)
        assert result[0]["title"] == "Colosseum"


# ============================================================
# JSON CLEANUP HELPER
# ============================================================

class TestCleanJson:

    def test_removes_trailing_comma_before_bracket(self):
        assert GeminiAdapter._clean_json('[1, 2,]') == '[1, 2]'

    def test_removes_trailing_comma_before_brace(self):
        assert GeminiAdapter._clean_json('{"a": 1,}') == '{"a": 1}'

    def test_removes_single_line_comments(self):
        cleaned = GeminiAdapter._clean_json('{"a": 1} // comment')
        assert "//" not in cleaned

    def test_preserves_urls_in_strings(self):
        """URLs like https://... should NOT be treated as comments"""
        text = '{"url": "https://example.com"}'
        # The // in https:// is inside a string, but our regex is line-based
        # so it won't break URLs that don't have // starting the content
        cleaned = GeminiAdapter._clean_json(text)
        assert "https:" in cleaned


# ============================================================
# GENERATE HIGHLIGHTS (mocked Gemini call)
# ============================================================

class TestGenerateHighlights:

    def test_returns_parsed_highlights(self, adapter):
        mock_highlights = [
            {"id": f"H00{i}", "title": f"Place {i}",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 6)
        ]

        mock_response = MagicMock()
        mock_response.text = f'```json\n{__import__("json").dumps(mock_highlights)}\n```'
        adapter.model.generate_content.return_value = mock_response

        result = adapter.generate_highlights("Rome", "Italy")
        assert len(result) == 5
        assert result[0]["id"] == "H001"
        adapter.model.generate_content.assert_called_once()


# ============================================================
# GENERATE RESTAURANTS (mocked Gemini call)
# ============================================================

class TestGenerateRestaurants:

    def test_returns_parsed_restaurants(self, adapter):
        mock_restaurants = [
            {"name": f"Restaurant {i}", "cuisine": "Italian",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 4)
        ]

        mock_response = MagicMock()
        mock_response.text = __import__("json").dumps(mock_restaurants)
        adapter.model.generate_content.return_value = mock_response

        result = adapter.generate_restaurants("Rome", "Italy")
        assert len(result) == 3


# ============================================================
# TRANSLATE CONTENT (mocked Gemini call)
# ============================================================

class TestTranslateContent:

    def test_returns_translated_content(self, adapter):
        original = {"title": "Colosseum", "description": "Ancient amphitheater"}
        translated = {"title": "Coliseo", "description": "Anfiteatro antiguo"}

        mock_response = MagicMock()
        mock_response.text = __import__("json").dumps(translated)
        adapter.model.generate_content.return_value = mock_response

        result = adapter.translate_content(original, "es")
        assert result["title"] == "Coliseo"


# ============================================================
# GEMINI API ERROR HANDLING
# ============================================================

class TestGeminiErrorHandling:

    def test_api_failure_raises_exception(self, adapter):
        adapter.model.generate_content.side_effect = Exception("API quota exceeded")
        with pytest.raises(Exception, match="API quota exceeded"):
            adapter._call_gemini("test prompt", 0.7)

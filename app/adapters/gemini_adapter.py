"""
Gemini Adapter — speed-optimised.

Changes for speed:
- max_output_tokens capped at 2048
- Prompts generate content directly in the target language
- No separate translation call needed for destination content
"""

import google.generativeai as genai
from typing import Dict, Any, List
from config.settings import get_settings
from config.constants import GEMINI_MODEL
from app.prompts.destination_prompts import (
    HighlightsPrompt, RestaurantsPrompt, TransportPrompt, NewsPrompt
)
from app.prompts.translation_prompts import TranslationPrompt
from app.prompts.base_prompts import PromptConfig
import json
import logging
import time

logger = logging.getLogger(__name__)


class GeminiAdapter:
    """Adapter for Google Gemini API using centralized prompts"""

    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def generate_highlights(self, city: str, country: str, language: str = "en") -> List[Dict[str, str]]:
        """Generate top 5 highlights — directly in the target language"""
        logger.info(f"Generating highlights for {city}, {country} in {language}")

        prompt = HighlightsPrompt.build(city, country, language)
        temperature = HighlightsPrompt.temperature()

        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)

    def generate_restaurants(self, city: str, country: str, language: str = "en") -> List[Dict[str, str]]:
        """Generate top 3 restaurants — directly in the target language"""
        logger.info(f"Generating restaurants for {city}, {country} in {language}")

        prompt = RestaurantsPrompt.build(city, country, language)
        temperature = RestaurantsPrompt.temperature()

        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)

    def generate_airport_transport(self, city: str, airport_code: str, language: str = "en") -> List[Dict[str, Any]]:
        """Generate transport options — directly in the target language"""
        logger.info(f"Generating transport for {airport_code} → {city} in {language}")

        prompt = TransportPrompt.build(city, airport_code, language)
        temperature = TransportPrompt.temperature()

        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)

    def generate_mock_news(self, city: str, language: str = "en") -> List[Dict[str, str]]:
        """Generate safe local news — directly in the target language"""
        logger.info(f"Generating news for {city} in {language}")

        prompt = NewsPrompt.build(city, language)
        temperature = NewsPrompt.temperature()

        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)

    def translate_content(self, content: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """Translate content using structure-preserving prompt (fallback only)"""
        logger.info(f"Translating content to {target_language}")

        prompt = TranslationPrompt.build(content, target_language)
        temperature = TranslationPrompt.temperature()

        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)

    def _call_gemini(self, prompt: str, temperature: float) -> str:
        """Make API call to Gemini with max_output_tokens for speed"""
        start = time.perf_counter()
        prompt_len = len(prompt)
        logger.info(f"  ⬆ GEMINI REQUEST — model={GEMINI_MODEL} temp={temperature} prompt_chars={prompt_len}")
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=PromptConfig.MAX_OUTPUT_TOKENS,
                )
            )
            text = response.text.strip()
            elapsed = round((time.perf_counter() - start) * 1000)
            logger.info(f"  ⬇ GEMINI RESPONSE — {elapsed}ms, response_chars={len(text)}")
            return text
        except Exception as e:
            elapsed = round((time.perf_counter() - start) * 1000)
            logger.error(f"  ✖ GEMINI ERROR — {elapsed}ms: {e}")
            raise

    def _parse_json_response(self, text: str) -> Any:
        """Parse JSON response, handling markdown code blocks"""
        # Remove markdown code blocks if present
        if text.startswith("```"):
            lines = text.split("\n")
            lines = lines[1:]
            if lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)

        text = text.strip().strip("`").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {text[:500]}")
            raise ValueError(f"Invalid JSON response from Gemini: {e}")


# Singleton instance
gemini_adapter = GeminiAdapter()

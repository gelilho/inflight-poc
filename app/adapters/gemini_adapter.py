"""
Gemini Adapter - Uses centralized prompts for all LLM interactions
"""

import google.generativeai as genai
from typing import Dict, Any, List
from config.settings import get_settings
from config.constants import GEMINI_MODEL
from app.prompts.destination_prompts import (
    HighlightsPrompt, RestaurantsPrompt, TransportPrompt, NewsPrompt
)
from app.prompts.translation_prompts import TranslationPrompt
import json
import logging

logger = logging.getLogger(__name__)


class GeminiAdapter:
    """Adapter for Google Gemini API using centralized prompts"""
    
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def generate_highlights(self, city: str, country: str) -> List[Dict[str, str]]:
        """Generate top 5 highlights using structured prompt"""
        logger.info(f"Generating highlights for {city}, {country}")
        
        prompt = HighlightsPrompt.build(city, country)
        temperature = HighlightsPrompt.temperature()
        
        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)
    
    def generate_restaurants(self, city: str, country: str) -> List[Dict[str, str]]:
        """Generate top 3 restaurants using structured prompt"""
        logger.info(f"Generating restaurants for {city}, {country}")
        
        prompt = RestaurantsPrompt.build(city, country)
        temperature = RestaurantsPrompt.temperature()
        
        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)
    
    def generate_airport_transport(self, city: str, airport_code: str) -> List[Dict[str, Any]]:
        """Generate transport options using structured prompt"""
        logger.info(f"Generating transport for {airport_code} → {city}")
        
        prompt = TransportPrompt.build(city, airport_code)
        temperature = TransportPrompt.temperature()
        
        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)
    
    def generate_mock_news(self, city: str) -> List[Dict[str, str]]:
        """Generate safe local news using structured prompt"""
        logger.info(f"Generating news for {city}")
        
        prompt = NewsPrompt.build(city)
        temperature = NewsPrompt.temperature()
        
        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)
    
    def translate_content(self, content: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """Translate content using structure-preserving prompt"""
        logger.info(f"Translating content to {target_language}")
        
        prompt = TranslationPrompt.build(content, target_language)
        temperature = TranslationPrompt.temperature()
        
        response = self._call_gemini(prompt, temperature)
        return self._parse_json_response(response)
    
    def _call_gemini(self, prompt: str, temperature: float) -> str:
        """Make API call to Gemini"""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature
                )
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            raise
    
    def _parse_json_response(self, text: str) -> Any:
        """Parse JSON response, handling markdown code blocks"""
        # Remove markdown code blocks if present
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```json or ```)
            lines = lines[1:]
            # Remove last line (```)
            if lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        
        # Clean up any remaining backticks
        text = text.strip().strip("`").strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response text: {text[:500]}")
            raise ValueError(f"Invalid JSON response from Gemini: {e}")


# Singleton instance
gemini_adapter = GeminiAdapter()

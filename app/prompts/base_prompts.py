"""
Base Prompt Templates for Gemini API
All LLM instructions are centralized here for easy management and tuning.
"""

from typing import Dict, Any


class BasePrompt:
    """Base class for all prompts with common patterns"""
    
    @staticmethod
    def json_output_rules() -> str:
        """Standard JSON output rules for all prompts"""
        return """
CRITICAL JSON OUTPUT RULES:
1. Return ONLY valid JSON (no markdown, no code blocks, no explanation)
2. Do NOT wrap response in ```json``` or ``` tags
3. Ensure all quotes are properly escaped
4. Validate JSON structure before returning
5. No additional text before or after JSON
"""
    
    @staticmethod
    def inflight_safety_rules() -> str:
        """Content safety rules for inflight use"""
        return """
INFLIGHT SAFETY CONTENT RULES:
1. Tone: Positive, welcoming, informative
2. NO dramatic content (violence, crime, disasters, terrorism)
3. NO controversial topics (politics, religion, sensitive social issues)
4. NO anxiety-inducing content (flight safety concerns, emergencies)
5. Keep content PG-rated and family-friendly
6. Focus on enrichment and destination excitement
"""
    
    @staticmethod
    def translation_preservation_rules() -> str:
        """Rules for structure-preserving translation"""
        return """
TRANSLATION STRUCTURE PRESERVATION RULES:
1. Keep EXACT JSON structure (all keys, all arrays)
2. Keep all IDs unchanged (H001, H002, etc.)
3. Keep all field names in English
4. Translate ONLY text values (titles, descriptions, names, notes)
5. Keep numbers, dates, coordinates unchanged
6. Maintain array lengths exactly
7. Do NOT add or remove any fields
"""


class PromptConfig:
    """Configuration for prompt behavior"""
    
    # Temperature settings
    CREATIVE_TEMPERATURE = 0.7  # For highlights, restaurants (more creative)
    FACTUAL_TEMPERATURE = 0.5   # For transport, news (more factual)
    TRANSLATION_TEMPERATURE = 0.3  # For translations (more consistent)
    
    # Content length guidelines
    BRIEF_DESCRIPTION_MAX_WORDS = 20
    LONG_DESCRIPTION_MIN_WORDS = 150
    LONG_DESCRIPTION_MAX_WORDS = 250
    
    # Cardinality
    HIGHLIGHTS_COUNT = 5
    RESTAURANTS_COUNT = 3
    TRANSPORT_OPTIONS_MAX = 3
    NEWS_COUNT = 5

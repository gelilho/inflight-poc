"""
Base Prompt Templates for Gemini API
All LLM instructions are centralized here for easy management and tuning.

Speed-optimised: short prompts, small outputs, low temperature.
"""

from typing import Dict, Any


class BasePrompt:
    """Base class for all prompts with common patterns"""

    @staticmethod
    def json_output_rules() -> str:
        return "Return ONLY valid JSON. No markdown, no code blocks, no explanation."

    @staticmethod
    def inflight_safety_rules() -> str:
        return "Tone: positive, family-friendly. NO violence, crime, politics, disasters, or anxiety-inducing content."

    @staticmethod
    def translation_preservation_rules() -> str:
        return (
            "Keep exact JSON structure, all keys/IDs unchanged. "
            "Translate ONLY text values. Keep numbers and field names in English."
        )


class PromptConfig:
    """Configuration for prompt behavior"""

    # Temperature — lower = faster + more deterministic
    CREATIVE_TEMPERATURE = 0.4
    FACTUAL_TEMPERATURE = 0.3
    TRANSLATION_TEMPERATURE = 0.2

    # Content length — SHORT for mobile screens and speed
    BRIEF_DESCRIPTION_MAX_WORDS = 15
    LONG_DESCRIPTION_MIN_WORDS = 40
    LONG_DESCRIPTION_MAX_WORDS = 80

    # Cardinality
    HIGHLIGHTS_COUNT = 5
    RESTAURANTS_COUNT = 3
    TRANSPORT_OPTIONS_MAX = 3
    NEWS_COUNT = 5

    # Max output tokens — enough for 5 highlights + 3 restaurants, but capped for speed
    MAX_OUTPUT_TOKENS = 4096

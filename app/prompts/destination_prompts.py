"""
Destination Content Generation Prompts — speed-optimised.

Key design decisions for fast responses:
- Short prompts (no verbose examples)
- Compact output (40-80 words per long_description)
- Generate directly in the target language (skip translation step!)
- Low temperature for faster sampling
"""

from app.prompts.base_prompts import BasePrompt, PromptConfig

# Map language codes to names for prompts
LANG_NAMES = {
    "es": "Spanish", "en": "English", "fr": "French",
    "it": "Italian", "ca": "Catalan", "gl": "Galician",
}


class HighlightsPrompt(BasePrompt):
    """Generate top 5 destination highlights"""

    @staticmethod
    def build(city: str, country: str, language: str = "en") -> str:
        lang = LANG_NAMES.get(language, "English")
        return f"""Generate 5 top places to visit in {city}, {country}. Write in {lang}.

Mix: cultural, historical, popular. Brief = 1 sentence ({PromptConfig.BRIEF_DESCRIPTION_MAX_WORDS} words max). Long = 2 short paragraphs ({PromptConfig.LONG_DESCRIPTION_MIN_WORDS}-{PromptConfig.LONG_DESCRIPTION_MAX_WORDS} words): what makes it special + practical tip.

{BasePrompt.inflight_safety_rules()}
{BasePrompt.json_output_rules()}

Return JSON array:
[{{"id":"H001","title":"...","brief_description":"...","long_description":"..."}}, ... ]

Exactly 5 items, IDs H001-H005."""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.CREATIVE_TEMPERATURE


class RestaurantsPrompt(BasePrompt):
    """Generate top 3 restaurant recommendations"""

    @staticmethod
    def build(city: str, country: str, language: str = "en") -> str:
        lang = LANG_NAMES.get(language, "English")
        return f"""Generate 3 restaurant recommendations in {city}, {country}. Write in {lang}.

Mix: local traditional (at least 1), different price ranges. Brief = 1 sentence ({PromptConfig.BRIEF_DESCRIPTION_MAX_WORDS} words max). Long = 2 short paragraphs ({PromptConfig.LONG_DESCRIPTION_MIN_WORDS}-{PromptConfig.LONG_DESCRIPTION_MAX_WORDS} words): signature dishes + practical info (price range, reservation tips).

{BasePrompt.inflight_safety_rules()}
{BasePrompt.json_output_rules()}

Return JSON array:
[{{"name":"...","cuisine":"...","brief_description":"...","long_description":"..."}}, ... ]

Exactly 3 restaurants."""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.CREATIVE_TEMPERATURE


class TransportPrompt(BasePrompt):
    """Generate airport transport options"""

    @staticmethod
    def build(city: str, airport_code: str, language: str = "en") -> str:
        lang = LANG_NAMES.get(language, "English")
        return f"""Transport options from {airport_code} airport to {city} center. Write in {lang}.

1-3 modes. IMPORTANT: mode MUST be exactly one of: "train", "bus", "taxi" (no other values).
Include duration and useful notes (cost, frequency, tips).

{BasePrompt.json_output_rules()}

Return JSON array:
[{{"mode":"train","estimated_duration_minutes":32,"notes":"..."}}, ... ]"""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.FACTUAL_TEMPERATURE


class NewsPrompt(BasePrompt):
    """Generate safe, relevant local news"""

    @staticmethod
    def build(city: str, language: str = "en") -> str:
        lang = LANG_NAMES.get(language, "English")
        return f"""Generate 5 positive local news headlines for {city}. Write in {lang}.

Categories: sports, culture, events, local_interest. Positive/neutral tone only.
Brief = 1 sentence. Long = 1-2 short paragraphs ({PromptConfig.LONG_DESCRIPTION_MIN_WORDS}-{PromptConfig.LONG_DESCRIPTION_MAX_WORDS} words).

{BasePrompt.inflight_safety_rules()}
{BasePrompt.json_output_rules()}

Return JSON array:
[{{"title":"...","brief_description":"...","long_description":"...","category":"sports"}}, ... ]

Exactly 5 items. Mix categories."""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.FACTUAL_TEMPERATURE


class WeatherPrompt(BasePrompt):
    """Generate a realistic 3-day weather forecast for a destination"""

    @staticmethod
    def build(city: str, language: str = "en") -> str:
        lang = LANG_NAMES.get(language, "English")
        return f"""Generate a realistic 3-day weather forecast for {city} starting from today. Write in {lang}.

Use typical weather patterns for this city and time of year. Be realistic with temperatures.
Conditions should be one of: Sunny, Partly Cloudy, Cloudy, Clear, Rain, Light Rain, Overcast, Windy.

{BasePrompt.json_output_rules()}

Return JSON array:
[{{"date":"YYYY-MM-DD","condition":"...","min_temperature_c":10.0,"max_temperature_c":18.0}}, ... ]

Exactly 3 days. Use today and next 2 days as dates."""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.FACTUAL_TEMPERATURE

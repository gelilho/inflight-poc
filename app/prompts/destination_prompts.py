"""
Destination Content Generation Prompts — speed-optimised.

Key design decisions for fast responses:
- Short prompts (no verbose examples)
- Compact output (40-80 words per long_description)
- Generate directly in the target language (skip translation step!)
- Low temperature for faster sampling
- Inject real dates (weather) so Gemini never hallucinates past dates
"""

from datetime import date, timedelta
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
        return f"""Generate 5 positive news headlines relevant to {city}. Write in {lang}.

IMPORTANT ordering:
- Item 1: general interest or worldwide relevance (culture, science, environment, technology)
- Items 2-5: mix of local_interest, culture, events, sports

Categories: sports, culture, events, local_interest. Positive/neutral tone only.
Brief = 1 sentence. Long = 1-2 short paragraphs ({PromptConfig.LONG_DESCRIPTION_MIN_WORDS}-{PromptConfig.LONG_DESCRIPTION_MAX_WORDS} words).

{BasePrompt.inflight_safety_rules()}
{BasePrompt.json_output_rules()}

Return JSON array:
[{{"title":"...","brief_description":"...","long_description":"...","category":"culture"}}, ... ]

Exactly 5 items. First item must NOT be sports."""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.FACTUAL_TEMPERATURE


class WeatherPrompt(BasePrompt):
    """Generate a realistic 3-day weather forecast for a destination"""

    @staticmethod
    def build(city: str, language: str = "en") -> str:
        lang = LANG_NAMES.get(language, "English")
        today = date.today()
        d1 = today.isoformat()
        d2 = (today + timedelta(days=1)).isoformat()
        d3 = (today + timedelta(days=2)).isoformat()
        return f"""Generate a realistic 3-day weather forecast for {city}. Write in {lang}.

Today is {d1}. Use these exact dates: {d1}, {d2}, {d3}.
Use typical weather patterns for this city and time of year. Be realistic with temperatures.
Conditions should be one of: Sunny, Partly Cloudy, Cloudy, Clear, Rain, Light Rain, Overcast, Windy.

{BasePrompt.json_output_rules()}

Return JSON array:
[{{"date":"{d1}","condition":"...","min_temperature_c":10.0,"max_temperature_c":18.0}}, ... ]

Exactly 3 days. Use the 3 dates above."""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.FACTUAL_TEMPERATURE

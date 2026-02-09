"""Fixed constants per environment"""

import os

# Supported languages for translation
SUPPORTED_LANGUAGES = ["es", "en", "fr", "it", "ca", "gl"]

# Airport coordinates (lat/lon — kept for reference)
AIRPORT_COORDINATES = {
    "FCO": {"lat": 41.8003, "lon": 12.2389},   # Rome Fiumicino
    "LHR": {"lat": 51.4700, "lon": -0.4543},   # London Heathrow
    "CDG": {"lat": 49.0097, "lon": 2.5479},     # Paris CDG
}

# City to country-code mapping
CITY_COUNTRY_CODES = {
    "Rome": "it",
    "London": "gb",
    "Paris": "fr",
}

# Cardinality constraints
HIGHLIGHTS_COUNT = 5
RESTAURANTS_COUNT = 3
CABIN_CREW_COUNT = 3
WEATHER_DAYS = 3
NEWS_COUNT = 5

# News categories (allowed)
ALLOWED_NEWS_CATEGORIES = ["sports", "culture", "events", "local_interest"]

# Gemini model configuration
GEMINI_MODEL = "models/gemini-2.5-flash"  # Latest and fastest!
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 2048

# Startup pre-warming — configurable via env vars or demo-config.json
# PREWARM_AIRPORTS: comma-separated airport codes (default: FCO)
# PREWARM_LANGUAGES: comma-separated language codes (default: en,es,it)
_raw_airports = os.environ.get("PREWARM_AIRPORTS", "FCO")
_raw_languages = os.environ.get("PREWARM_LANGUAGES", "en,es,it")
PREWARM_AIRPORTS = [a.strip() for a in _raw_airports.split(",") if a.strip()]
PREWARM_LANGUAGES = [l.strip() for l in _raw_languages.split(",") if l.strip()]

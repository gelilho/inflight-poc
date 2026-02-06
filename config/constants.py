"""Fixed constants per environment"""

# Supported languages for translation
SUPPORTED_LANGUAGES = ["es", "en", "fr", "it", "ca", "gl"]

# Cardinality constraints
HIGHLIGHTS_COUNT = 5
RESTAURANTS_COUNT = 3
CABIN_CREW_COUNT = 3
WEATHER_DAYS = 3
NEWS_COUNT = 5

# News categories (allowed)
ALLOWED_NEWS_CATEGORIES = ["sports", "culture", "events", "local_interest"]

# Gemini model configuration
GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_TEMPERATURE = 0.7
GEMINI_MAX_TOKENS = 2048

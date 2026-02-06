import google.generativeai as genai
from typing import Dict, Any, List
from config.settings import get_settings
from config.constants import GEMINI_MODEL, GEMINI_TEMPERATURE
import json


class GeminiAdapter:
    """Adapter for Google Gemini API"""
    
    def __init__(self):
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
    
    def generate_highlights(self, city: str, country: str) -> List[Dict[str, str]]:
        """Generate top 5 highlights with brief AND long descriptions"""
        prompt = f"""Generate exactly 5 top places to visit in {city}, {country}.

Return ONLY valid JSON in this exact format (no markdown, no explanation):
[
  {{
    "id": "H001",
    "title": "Place Name",
    "brief_description": "One compelling sentence that captures the essence",
    "long_description": "2-3 paragraphs with rich detail about history, what to see, visiting tips, best time to visit, and why it's special. Make it engaging and informative for travelers."
  }},
  {{
    "id": "H002",
    "title": "Place Name",
    "brief_description": "One compelling sentence",
    "long_description": "2-3 detailed paragraphs..."
  }},
  {{
    "id": "H003",
    "title": "Place Name",
    "brief_description": "One compelling sentence",
    "long_description": "2-3 detailed paragraphs..."
  }},
  {{
    "id": "H004",
    "title": "Place Name",
    "brief_description": "One compelling sentence",
    "long_description": "2-3 detailed paragraphs..."
  }},
  {{
    "id": "H005",
    "title": "Place Name",
    "brief_description": "One compelling sentence",
    "long_description": "2-3 detailed paragraphs..."
  }}
]

Requirements:
- Exactly 5 items, IDs H001-H005
- Mix cultural, historical, and popular attractions
- Brief: 1 sentence, max 20 words
- Long: 2-3 paragraphs, 150-250 words total
- Inflight-appropriate tone"""

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_TEMPERATURE
            )
        )
        
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        return json.loads(text.strip())
    
    def generate_restaurants(self, city: str, country: str) -> List[Dict[str, str]]:
        """Generate top 3 restaurants with brief AND long descriptions"""
        prompt = f"""Generate exactly 3 restaurant recommendations in {city}, {country}.

Return ONLY valid JSON in this exact format (no markdown, no explanation):
[
  {{
    "name": "Restaurant Name",
    "cuisine": "Type of Cuisine",
    "brief_description": "One sentence highlighting signature dish or atmosphere",
    "long_description": "2-3 paragraphs describing the restaurant's history, ambiance, signature dishes, price range, location tips, and why locals/travelers love it. Make it mouth-watering and helpful."
  }},
  {{
    "name": "Restaurant Name",
    "cuisine": "Type",
    "brief_description": "One sentence",
    "long_description": "2-3 detailed paragraphs..."
  }},
  {{
    "name": "Restaurant Name",
    "cuisine": "Type",
    "brief_description": "One sentence",
    "long_description": "2-3 detailed paragraphs..."
  }}
]

Requirements:
- Exactly 3 restaurants
- Variety of cuisines (include local cuisine)
- Brief: 1 sentence, max 20 words
- Long: 2-3 paragraphs, 150-250 words total
- Mention price range and location"""

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_TEMPERATURE
            )
        )
        
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        return json.loads(text.strip())
    
    def generate_airport_transport(self, city: str, airport_code: str) -> List[Dict[str, Any]]:
        """Generate transport options from airport to main train station"""
        prompt = f"""Generate transport options from {airport_code} airport to the main train station in {city}.

Return ONLY valid JSON in this exact format (no markdown, no explanation):
[
  {{"mode": "train", "estimated_duration_minutes": 30, "notes": "Brief practical note with cost and frequency"}},
  {{"mode": "bus", "estimated_duration_minutes": 45, "notes": "Brief practical note"}},
  {{"mode": "taxi", "estimated_duration_minutes": 25, "notes": "Brief practical note"}}
]

Requirements:
- 1-3 options (most common modes)
- mode: "train", "bus", or "taxi"
- Realistic duration estimates
- Notes: frequency, approx cost, practical tips"""

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_TEMPERATURE
            )
        )
        
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        return json.loads(text.strip())
    
    def generate_mock_news(self, city: str) -> List[Dict[str, str]]:
        """Generate mock local news with brief AND long descriptions"""
        prompt = f"""Generate exactly 5 recent local news headlines for {city}.

Return ONLY valid JSON in this exact format (no markdown, no explanation):
[
  {{
    "title": "Headline",
    "brief_description": "One sentence summary",
    "long_description": "2-3 paragraphs with full story details, context, quotes if relevant, and local impact. Make it informative and engaging.",
    "category": "sports"
  }},
  {{
    "title": "Headline",
    "brief_description": "One sentence",
    "long_description": "2-3 paragraphs...",
    "category": "culture"
  }},
  {{
    "title": "Headline",
    "brief_description": "One sentence",
    "long_description": "2-3 paragraphs...",
    "category": "events"
  }},
  {{
    "title": "Headline",
    "brief_description": "One sentence",
    "long_description": "2-3 paragraphs...",
    "category": "local_interest"
  }},
  {{
    "title": "Headline",
    "brief_description": "One sentence",
    "long_description": "2-3 paragraphs...",
    "category": "sports"
  }}
]

Requirements:
- Exactly 5 items
- category: "sports", "culture", "events", or "local_interest"
- NO dramatic content (no crime, violence, disasters)
- Positive or neutral tone only
- Brief: 1 sentence
- Long: 2-3 paragraphs, 150-200 words
- Recent/timely topics"""

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=GEMINI_TEMPERATURE
            )
        )
        
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        return json.loads(text.strip())
    
    def translate_content(self, content: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """Translate destination experience content preserving structure"""
        
        language_names = {
            "es": "Spanish",
            "en": "English",
            "fr": "French",
            "it": "Italian",
            "ca": "Catalan",
            "gl": "Galician"
        }
        
        prompt = f"""Translate the following content to {language_names[target_language]}.

CRITICAL RULES:
1. Preserve EXACT JSON structure
2. Keep all IDs unchanged (H001, H002, etc.)
3. Keep all field names in English
4. Translate ONLY the text values (titles, descriptions, names, etc.)
5. Keep numbers, dates unchanged
6. Return ONLY valid JSON (no markdown, no explanation)

Content to translate:
{json.dumps(content, indent=2, ensure_ascii=False)}

Return the translated JSON:"""

        response = self.model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3  # Lower for translation accuracy
            )
        )
        
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        
        return json.loads(text.strip())


# Singleton instance
gemini_adapter = GeminiAdapter()

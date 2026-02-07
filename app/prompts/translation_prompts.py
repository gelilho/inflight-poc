"""
Translation Prompts
Structure-preserving translation for all destination content.
"""

from typing import Dict, Any
import json
from app.prompts.base_prompts import BasePrompt, PromptConfig


class TranslationPrompt(BasePrompt):
    """Prompt for translating content while preserving JSON structure"""
    
    LANGUAGE_NAMES = {
        "es": "Spanish (Spain)",
        "en": "English",
        "fr": "French (France)",
        "it": "Italian (Italy)",
        "ca": "Catalan",
        "gl": "Galician"
    }
    
    @staticmethod
    def build(content: Dict[str, Any], target_language: str) -> str:
        language_name = TranslationPrompt.LANGUAGE_NAMES.get(target_language, target_language)
        
        return f"""You are a professional translator specializing in travel content translation.

TASK: Translate the following destination content to {language_name}.

{TranslationPrompt.translation_preservation_rules()}

TRANSLATION GUIDELINES:
1. LANGUAGE-SPECIFIC CONSIDERATIONS:
   - Spanish (es): Use formal "usted" form, Spanish from Spain vocabulary
   - Catalan (ca): Use authentic Catalan, not Spanish transliteration
   - Galician (gl): Use authentic Galician, maintain regional character
   - French (fr): Use formal register, French from France
   - Italian (it): Use standard Italian, maintain elegance
   - English (en): Use clear, accessible language

2. CONTENT-SPECIFIC RULES:
   - Place names: Keep original if widely known (Colosseum), translate if descriptive (Trevi Fountain → Fontana di Trevi)
   - Dishes: Keep original name + translate description
   - Street names: Keep original
   - Historical figures: Use target language convention if it exists
   - Measurements: Keep metric units as-is

3. TONE & STYLE:
   - Maintain the same level of formality
   - Preserve enthusiasm and descriptive richness
   - Adapt idioms culturally (don't translate literally)
   - Keep the same information density

{BasePrompt.json_output_rules()}

CONTENT TO TRANSLATE:
{json.dumps(content, indent=2, ensure_ascii=False)}

CRITICAL VALIDATIONS:
- Same number of highlights (if present)
- Same number of restaurants (if present)
- Same number of transport options (if present)
- Same number of news items (if present)
- All IDs unchanged (H001, H002, etc.)
- All field names in English
- No new fields added
- No fields removed

Return the complete translated JSON structure.
"""
    
    @staticmethod
    def temperature() -> float:
        return PromptConfig.TRANSLATION_TEMPERATURE

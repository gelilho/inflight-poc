# 🤖 LLM Prompts Module

All Gemini API prompts are centralized here for easy management, tuning, and auditing.

## Structure
```
app/prompts/
├── base_prompts.py          # Base rules and configuration
├── destination_prompts.py   # Content generation prompts
├── translation_prompts.py   # Translation prompts
└── README.md               # This file
```

## Prompt Categories

### 1. **Destination Content** (`destination_prompts.py`)

#### **HighlightsPrompt**
- **Purpose:** Generate top 5 places to visit
- **Temperature:** 0.7 (creative)
- **Output:** 5 highlights with brief + long descriptions
- **Rules:** Mix of cultural/historical/popular, avoid generic phrases

#### **RestaurantsPrompt**
- **Purpose:** Generate top 3 restaurant recommendations
- **Temperature:** 0.7 (creative)
- **Output:** 3 restaurants with brief + long descriptions
- **Rules:** Include local cuisine, variety of price ranges

#### **TransportPrompt**
- **Purpose:** Generate airport transport options
- **Temperature:** 0.5 (factual)
- **Output:** 1-3 transport modes with duration + practical notes
- **Rules:** Accurate info, cost estimates, service frequency

#### **NewsPrompt**
- **Purpose:** Generate safe, relevant local news
- **Temperature:** 0.5 (factual)
- **Output:** 5 news items with brief + long descriptions
- **Rules:** NO violence/crime/disasters, positive/neutral only

### 2. **Translation** (`translation_prompts.py`)

#### **TranslationPrompt**
- **Purpose:** Translate while preserving JSON structure
- **Temperature:** 0.3 (consistent)
- **Output:** Translated content with same structure
- **Rules:** Keep IDs, field names, array lengths unchanged

## Base Rules (`base_prompts.py`)

### **JSON Output Rules**
- No markdown wrappers
- Valid JSON only
- No explanatory text

### **Inflight Safety Rules**
- Positive/welcoming tone
- NO dramatic content
- NO anxiety-inducing topics
- PG-rated, family-friendly

### **Translation Preservation Rules**
- Exact structure match
- IDs unchanged
- Field names in English
- Only text values translated

## Configuration

### **PromptConfig** class defines:
- Temperature settings per prompt type
- Content length guidelines
- Cardinality constraints
```python
CREATIVE_TEMPERATURE = 0.7   # Highlights, restaurants
FACTUAL_TEMPERATURE = 0.5    # Transport, news
TRANSLATION_TEMPERATURE = 0.3 # Translations

BRIEF_DESCRIPTION_MAX_WORDS = 20
LONG_DESCRIPTION_MIN_WORDS = 150
LONG_DESCRIPTION_MAX_WORDS = 250
```

## How to Modify Prompts

### 1. **Adjust Tone/Style:**
Edit the instruction text in specific prompt classes.

### 2. **Change Content Rules:**
Modify the REQUIREMENTS section in each prompt.

### 3. **Update Examples:**
Change the OUTPUT FORMAT examples to guide Gemini.

### 4. **Tune Temperature:**
Adjust `temperature()` method return value:
- 0.0-0.3: Very consistent, factual
- 0.4-0.7: Balanced
- 0.8-1.0: Creative, varied

### 5. **Add New Prompt:**
Create new class inheriting from `BasePrompt`:
```python
class MyNewPrompt(BasePrompt):
    @staticmethod
    def build(param1: str, param2: str) -> str:
        return f"""[Your prompt here]
        
        {BasePrompt.inflight_safety_rules()}
        {BasePrompt.json_output_rules()}
        """
    
    @staticmethod
    def temperature() -> float:
        return 0.6
```

## Testing Prompts

To test a prompt in isolation:
```python
from app.prompts.destination_prompts import HighlightsPrompt

prompt = HighlightsPrompt.build("Rome", "Italy")
print(prompt)  # Review the prompt
```

## Best Practices

1. ✅ **Be Specific:** Clear instructions = better output
2. ✅ **Use Examples:** Show desired format explicitly
3. ✅ **Validate Structure:** Always include JSON rules
4. ✅ **Set Constraints:** Specify exact counts, lengths
5. ✅ **Safety First:** Always include inflight safety rules
6. ✅ **Test Thoroughly:** Check edge cases and error handling

## Version Control

All prompts are versioned with the codebase. When modifying:
- Document WHY you changed it
- Test with multiple cities/scenarios
- Check output quality before deploying

---

**Last Updated:** 2026-02-06
**Owned by:** Product & Engineering Team

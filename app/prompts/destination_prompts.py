"""
Destination Content Generation Prompts
Step-by-step instructions for Gemini to generate destination content.
"""

from app.prompts.base_prompts import BasePrompt, PromptConfig


class HighlightsPrompt(BasePrompt):
    """Prompt for generating top 5 destination highlights"""
    
    @staticmethod
    def build(city: str, country: str) -> str:
        return f"""You are a professional travel content writer creating destination highlights for an airline's inflight entertainment system.

TASK: Generate exactly 5 top places to visit in {city}, {country}.

REQUIREMENTS:
1. SELECT ATTRACTIONS:
   - Mix of cultural, historical, and popular sites
   - Include both iconic landmarks and hidden gems
   - Ensure variety (not all museums, not all outdoor)
   - Consider different interests (history, art, food, architecture)

2. BRIEF DESCRIPTION (1 sentence, max {PromptConfig.BRIEF_DESCRIPTION_MAX_WORDS} words):
   - Capture the essence and appeal
   - Make it compelling and specific
   - Avoid generic phrases like "must-see" or "beautiful"
   - Example: "Ancient amphitheater where gladiators fought, showcasing Imperial Rome's grandeur"

3. LONG DESCRIPTION ({PromptConfig.LONG_DESCRIPTION_MIN_WORDS}-{PromptConfig.LONG_DESCRIPTION_MAX_WORDS} words, 2-3 paragraphs):
   - Paragraph 1: History and significance (what makes it special)
   - Paragraph 2: What visitors will see/experience (specific details)
   - Paragraph 3: Practical tips (best time to visit, insider advice)
   - Use engaging, storytelling language
   - Include specific architectural details, historical facts, or unique features
   - Make readers excited to visit

{BasePrompt.inflight_safety_rules()}

{BasePrompt.json_output_rules()}

OUTPUT FORMAT (exactly 5 items):
[
  {{
    "id": "H001",
    "title": "Colosseum",
    "brief_description": "Ancient amphitheater where gladiators fought, showcasing Imperial Rome's grandeur",
    "long_description": "The Colosseum, also known as the Flavian Amphitheatre, stands as Rome's most iconic monument and a testament to the engineering prowess of ancient Rome. Built between 70-80 AD under emperors Vespasian and Titus, this massive structure could hold up to 50,000 spectators who gathered to witness gladiatorial contests, animal hunts, and mock naval battles. The elliptical design, rising four stories high with a complex system of vaults and arches, influenced stadium architecture for centuries to come.\\n\\nVisitors today can walk through the arena floor where gladiators once stood, explore the underground hypogeum where animals and fighters waited, and climb to the upper tiers for panoramic views of ancient Rome. The partially ruined state actually adds to its majesty, revealing the sophisticated construction techniques including the use of concrete, travertine, and brick.\\n\\nFor the best experience, book tickets online to skip long queues, and visit early morning or late afternoon to avoid crowds and harsh midday sun. Consider a guided tour to truly appreciate the historical significance and architectural innovations. The nearby Roman Forum and Palatine Hill are included in combination tickets, making for a full day of ancient exploration."
  }},
  {{
    "id": "H002",
    "title": "[Place Name]",
    "brief_description": "[One compelling sentence]",
    "long_description": "[2-3 detailed paragraphs as described above]"
  }},
  {{
    "id": "H003",
    "title": "[Place Name]",
    "brief_description": "[One compelling sentence]",
    "long_description": "[2-3 detailed paragraphs]"
  }},
  {{
    "id": "H004",
    "title": "[Place Name]",
    "brief_description": "[One compelling sentence]",
    "long_description": "[2-3 detailed paragraphs]"
  }},
  {{
    "id": "H005",
    "title": "[Place Name]",
    "brief_description": "[One compelling sentence]",
    "long_description": "[2-3 detailed paragraphs]"
  }}
]

CRITICAL: Ensure exactly 5 highlights with IDs H001 through H005.
"""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.CREATIVE_TEMPERATURE


class RestaurantsPrompt(BasePrompt):
    """Prompt for generating top 3 restaurant recommendations"""
    
    @staticmethod
    def build(city: str, country: str) -> str:
        return f"""You are a professional food & travel writer creating restaurant recommendations for an airline's inflight entertainment system.

TASK: Generate exactly 3 restaurant recommendations in {city}, {country}.

REQUIREMENTS:
1. SELECT RESTAURANTS:
   - Include LOCAL/TRADITIONAL cuisine (mandatory - at least 1)
   - Mix of price ranges (include at least one mid-range option)
   - Variety of atmospheres (fine dining, casual, neighborhood gem)
   - Known for specific dishes or unique dining experiences
   - Avoid international chains

2. BRIEF DESCRIPTION (1 sentence, max {PromptConfig.BRIEF_DESCRIPTION_MAX_WORDS} words):
   - Highlight signature dish OR dining atmosphere
   - Make it mouth-watering and specific
   - Example: "Family-run trattoria serving authentic carbonara in a cozy Trastevere setting"

3. LONG DESCRIPTION ({PromptConfig.LONG_DESCRIPTION_MIN_WORDS}-{PromptConfig.LONG_DESCRIPTION_MAX_WORDS} words, 2-3 paragraphs):
   - Paragraph 1: Restaurant background (history, chef, philosophy, neighborhood)
   - Paragraph 2: Menu highlights (signature dishes, ingredients, cooking style, what to order)
   - Paragraph 3: Practical details (price range, location, reservation tips, dress code)
   - Use sensory language (flavors, aromas, textures)
   - Include specific dish recommendations

{BasePrompt.inflight_safety_rules()}

{BasePrompt.json_output_rules()}

OUTPUT FORMAT (exactly 3 restaurants):
[
  {{
    "name": "Da Enzo al 29",
    "cuisine": "Traditional Roman",
    "brief_description": "Family-run trattoria serving authentic Roman classics in charming Trastevere",
    "long_description": "Tucked away in the charming cobblestoned streets of Trastevere, Da Enzo al 29 has been a neighborhood institution for decades. This family-run trattoria embodies everything that makes Roman dining special: simple, seasonal ingredients transformed into soul-satisfying dishes through generations of culinary wisdom. The intimate space, with only about a dozen tables covered in red-checked cloth, fills quickly with locals and in-the-know visitors.\\n\\nThe menu changes daily based on market availability, but signature dishes like cacio e pepe (pecorino cheese and black pepper pasta), amatriciana, and saltimbocca alla romana are constants. The carciofi alla giudia (Jewish-style fried artichokes) are legendary when in season. Everything is made in-house, from the pasta to the tiramisu, and portions are generous in the best Roman tradition. The wine list focuses on regional Lazio producers, offering excellent value.\\n\\nExpect to spend €25-35 per person for a full meal with wine. Reservations are essential (they open at 12:30 for lunch, 7:30 for dinner) as walk-ins rarely get tables. The atmosphere is casual but arrives on time as they run a tight ship. Cash only. Located at Via dei Vascellari 29, it's a short walk from Piazza Santa Maria in Trastevere."
  }},
  {{
    "name": "[Restaurant Name]",
    "cuisine": "[Cuisine Type]",
    "brief_description": "[One compelling sentence]",
    "long_description": "[2-3 detailed paragraphs as described above]"
  }},
  {{
    "name": "[Restaurant Name]",
    "cuisine": "[Cuisine Type]",
    "brief_description": "[One compelling sentence]",
    "long_description": "[2-3 detailed paragraphs]"
  }}
]

CRITICAL: Ensure exactly 3 restaurants with variety in cuisine and price range.
"""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.CREATIVE_TEMPERATURE


class TransportPrompt(BasePrompt):
    """Prompt for generating airport transport options"""
    
    @staticmethod
    def build(city: str, airport_code: str) -> str:
        return f"""You are a practical travel advisor providing accurate transport information for airline passengers.

TASK: Provide transport options from {airport_code} airport to the main train station in {city}.

REQUIREMENTS:
1. SELECT TRANSPORT MODES (1-3 most common/practical):
   - Train (if available)
   - Bus (public or express)
   - Taxi (or rideshare)
   - Order by recommendation (fastest/most convenient first)

2. FOR EACH OPTION PROVIDE:
   - Mode: Must be exactly "train", "bus", or "taxi"
   - Duration: Realistic estimate in minutes (account for traffic/waiting)
   - Notes: Practical information including:
     * Service frequency (e.g., "every 15 minutes")
     * Approximate cost (in local currency with € equivalent if applicable)
     * Where to find it at airport (terminal, floor)
     * Ticket purchase info
     * Operating hours if limited
     * Any important tips

{BasePrompt.inflight_safety_rules()}

{BasePrompt.json_output_rules()}

OUTPUT FORMAT (1-3 options):
[
  {{
    "mode": "train",
    "estimated_duration_minutes": 32,
    "notes": "Leonardo Express runs every 15-30 minutes (5:35 AM - 11:35 PM). Tickets €14, purchase at machines in Terminal 3 arrivals or online. Direct service to Roma Termini with no stops. Most convenient option for city center."
  }},
  {{
    "mode": "bus",
    "estimated_duration_minutes": 55,
    "notes": "Terravision and other bus services (€6-8) depart from outside terminals every 30-40 minutes. Slower but economical. Buy tickets online or from driver (cash/card)."
  }},
  {{
    "mode": "taxi",
    "estimated_duration_minutes": 45,
    "notes": "Fixed fare €48 to city center (valid for up to 4 passengers with luggage). Official white taxis only - taxi stand outside arrivals. 30-60 min depending on traffic. No meters for airport rides."
  }}
]

CRITICAL: Provide accurate, current information. Duration should account for real conditions.
"""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.FACTUAL_TEMPERATURE


class NewsPrompt(BasePrompt):
    """Prompt for generating safe, relevant local news"""
    
    @staticmethod
    def build(city: str) -> str:
        return f"""You are a news editor curating local headlines for an airline's inflight entertainment system.

TASK: Generate exactly 5 recent local news headlines for {city}.

REQUIREMENTS:
1. NEWS SELECTION:
   - Recent topics (as if from the last 7 days)
   - Local relevance (city-specific, not national/international)
   - Mix categories: sports, culture, events, local_interest
   - Positive or neutral tone ONLY

2. CONTENT FILTERING (CRITICAL):
   EXCLUDE COMPLETELY:
   - Violence, crime, accidents, deaths
   - Political controversies or partisan content  
   - Disasters, fires, medical emergencies
   - Terrorism, war, conflict
   - Scandals, corruption
   - Economic downturns, layoffs
   - ANY anxiety-inducing content
   
   INCLUDE:
   - Sports victories, team news, player transfers
   - Cultural events, museum exhibitions, festivals
   - New restaurant/venue openings
   - City improvements, infrastructure (positive angle)
   - Local achievements, awards
   - Community celebrations

3. BRIEF DESCRIPTION (1 sentence):
   - Summarize the key point
   - Maintain positive/neutral tone

4. LONG DESCRIPTION ({PromptConfig.LONG_DESCRIPTION_MIN_WORDS}-{PromptConfig.LONG_DESCRIPTION_MAX_WORDS} words, 2-3 paragraphs):
   - Paragraph 1: What happened (the news event)
   - Paragraph 2: Context and details (why it matters, background)
   - Paragraph 3: Impact or what's next (future implications, dates)
   - Write as if for a general newspaper
   - Include quotes if relevant (can be paraphrased/generic)

5. CATEGORIES (must be one of):
   - "sports" - team news, matches, player updates
   - "culture" - arts, museums, theater, music, literature
   - "events" - festivals, celebrations, openings, exhibitions
   - "local_interest" - community news, city developments, human interest

{BasePrompt.inflight_safety_rules()}

{BasePrompt.json_output_rules()}

OUTPUT FORMAT (exactly 5 news items):
[
  {{
    "title": "AS Roma Secures Victory in Derby della Capitale",
    "brief_description": "Roma defeats Lazio 2-1 in thrilling match at Stadio Olimpico",
    "long_description": "AS Roma emerged victorious in Sunday's highly anticipated Derby della Capitale, defeating city rivals Lazio 2-1 in a thrilling encounter at the Stadio Olimpico. Goals from Paulo Dybala and Lorenzo Pellegrini secured the three points for the Giallorossi, delighting the home crowd of 65,000 fans in what was one of the season's most intense matches.\\n\\nThe victory marks Roma's third consecutive win in the derby and moves them up to fourth place in the Serie A standings. Manager José Mourinho praised his team's tactical discipline and fighting spirit, noting that the win demonstrates the squad's growing maturity and championship aspirations. Dybala's opening goal came from a brilliant counter-attack in the 23rd minute, while Pellegrini sealed the win with a clinical finish in the 78th minute.\\n\\nThe result sets up Roma well for their upcoming Champions League fixture and has energized the fanbase ahead of a crucial period in the season. The team returns to action on Wednesday against Napoli in what promises to be another significant test of their top-four ambitions.",
    "category": "sports"
  }},
  {{
    "title": "[Headline]",
    "brief_description": "[One sentence]",
    "long_description": "[2-3 paragraphs]",
    "category": "culture"
  }},
  {{
    "title": "[Headline]",
    "brief_description": "[One sentence]",
    "long_description": "[2-3 paragraphs]",
    "category": "events"
  }},
  {{
    "title": "[Headline]",
    "brief_description": "[One sentence]",
    "long_description": "[2-3 paragraphs]",
    "category": "local_interest"
  }},
  {{
    "title": "[Headline]",
    "brief_description": "[One sentence]",
    "long_description": "[2-3 paragraphs]",
    "category": "sports"
  }}
]

CRITICAL: Ensure exactly 5 news items. Mix categories. NO dramatic/negative content.
"""

    @staticmethod
    def temperature() -> float:
        return PromptConfig.FACTUAL_TEMPERATURE

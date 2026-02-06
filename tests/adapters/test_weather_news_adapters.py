"""Test Weather and News Adapters - Verify API integration works"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from app.adapters.weather_adapter import weather_adapter
from app.adapters.news_adapter import news_adapter

load_dotenv()

print("🧪 Testing Weather & News Adapters")
print("=" * 60)

# Test Weather Adapter
print("\n1️⃣  Testing: Weather Adapter (OpenWeatherMap)")
print("-" * 60)

try:
    print("Fetching 3-day forecast for Rome (FCO)...")
    weather = weather_adapter.get_forecast("FCO", days=3)
    
    if not weather:
        print("❌ FAILED: No weather data returned")
        sys.exit(1)
    
    print(f"✅ Successfully fetched {len(weather)} days of weather")
    
    print("\nWeather data sample:")
    for i, day in enumerate(weather):
        print(f"\n  Day {i+1}:")
        print(f"    Date: {day.get('date')}")
        print(f"    Condition: {day.get('condition')}")
        print(f"    Min Temp: {day.get('min_temperature_c')}°C")
        print(f"    Max Temp: {day.get('max_temperature_c')}°C")
    
    print("\n✅ Weather adapter validation passed")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test News Adapter
print("\n2️⃣  Testing: News Adapter (NewsAPI)")
print("-" * 60)

try:
    print("Fetching 5 news items for Rome...")
    news = news_adapter.get_local_news("Rome", limit=5)
    
    if not news:
        print("❌ FAILED: No news data returned")
        sys.exit(1)
    
    print(f"✅ Successfully fetched {len(news)} news items")
    
    print("\nNews data sample:")
    for i, item in enumerate(news[:2]):
        print(f"\n  News {i+1}:")
        print(f"    Title: {item.get('title', '')[:80]}...")
        print(f"    Category: {item.get('category')}")
        print(f"    Brief: {item.get('brief_description', '')[:80]}...")
    
    print("\n✅ News adapter validation passed")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("🎉 ALL ADAPTER TESTS PASSED!")
print("=" * 60)

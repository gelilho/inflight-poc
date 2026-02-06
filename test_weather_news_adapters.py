"""Test Weather and News Adapters - Verify API integration works"""

import sys
from dotenv import load_dotenv
from app.adapters.weather_adapter import weather_adapter
from app.adapters.news_adapter import news_adapter

load_dotenv()

print("🧪 Testing Weather & News Adapters")
print("=" * 60)

# ============================================================
# Test Weather Adapter
# ============================================================

print("\n1️⃣  Testing: Weather Adapter (OpenWeatherMap)")
print("-" * 60)

try:
    # Test for Rome (FCO)
    print("Fetching 3-day forecast for Rome (FCO)...")
    weather = weather_adapter.get_forecast("FCO", days=3)
    
    if not weather:
        print("❌ FAILED: No weather data returned")
        sys.exit(1)
    
    print(f"✅ Successfully fetched {len(weather)} days of weather")
    
    # Verify structure
    if len(weather) != 3:
        print(f"⚠️  WARNING: Expected 3 days, got {len(weather)}")
    
    print("\nWeather data sample:")
    for i, day in enumerate(weather):
        print(f"\n  Day {i+1}:")
        print(f"    Date: {day.get('date')}")
        print(f"    Condition: {day.get('condition')}")
        print(f"    Min Temp: {day.get('min_temperature_c')}°C")
        print(f"    Max Temp: {day.get('max_temperature_c')}°C")
        
        # Validate fields
        required_fields = ['date', 'condition', 'min_temperature_c', 'max_temperature_c']
        for field in required_fields:
            if field not in day:
                print(f"    ❌ Missing field: {field}")
                sys.exit(1)
    
    print("\n✅ Weather adapter validation passed")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# Test News Adapter
# ============================================================

print("\n2️⃣  Testing: News Adapter (NewsAPI)")
print("-" * 60)

try:
    # Test for Rome
    print("Fetching 5 news items for Rome...")
    news = news_adapter.get_local_news("Rome", limit=5)
    
    if not news:
        print("❌ FAILED: No news data returned")
        sys.exit(1)
    
    print(f"✅ Successfully fetched {len(news)} news items")
    
    # Verify structure
    if len(news) != 5:
        print(f"⚠️  WARNING: Expected 5 items, got {len(news)}")
    
    print("\nNews data sample:")
    for i, item in enumerate(news[:2]):  # Show first 2
        print(f"\n  News {i+1}:")
        print(f"    Title: {item.get('title', '')[:80]}...")
        print(f"    Category: {item.get('category')}")
        print(f"    Brief: {item.get('brief_description', '')[:80]}...")
        print(f"    Long: {item.get('long_description', '')[:100]}...")
        
        # Validate fields
        required_fields = ['title', 'brief_description', 'long_description', 'category']
        for field in required_fields:
            if field not in item:
                print(f"    ❌ Missing field: {field}")
                sys.exit(1)
        
        # Validate category
        allowed_categories = ['sports', 'culture', 'events', 'local_interest']
        if item['category'] not in allowed_categories:
            print(f"    ❌ Invalid category: {item['category']}")
            sys.exit(1)
    
    print("\n✅ News adapter validation passed")
    
except Exception as e:
    print(f"❌ FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============================================================
# Test Multiple Destinations
# ============================================================

print("\n3️⃣  Testing: Multiple Destinations")
print("-" * 60)

destinations = [
    ("FCO", "Rome"),
    ("LHR", "London"),
    ("CDG", "Paris")
]

for airport_code, city_name in destinations:
    try:
        print(f"\nTesting {city_name} ({airport_code})...")
        
        # Weather
        weather = weather_adapter.get_forecast(airport_code, days=3)
        print(f"  ✅ Weather: {len(weather)} days")
        
        # News
        news = news_adapter.get_local_news(city_name, limit=5)
        print(f"  ✅ News: {len(news)} items")
        
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        sys.exit(1)

print("\n✅ All destinations tested successfully")

# ============================================================
# Summary
# ============================================================

print("\n" + "=" * 60)
print("🎉 ALL ADAPTER TESTS PASSED!")
print("=" * 60)
print("\n✅ Weather adapter working (OpenWeatherMap)")
print("✅ News adapter working (NewsAPI or Gemini fallback)")
print("✅ Data structure validation passed")
print("✅ Multiple destinations supported")
print("\n🚀 Ready to test full API endpoints!")

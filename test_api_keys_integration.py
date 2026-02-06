"""Integration Tests - Verify ALL API keys (non-blocking)"""

import sys
from dotenv import load_dotenv
import os

load_dotenv()

# Track results
results = {
    "gemini": {"status": "pending", "message": ""},
    "weather": {"status": "pending", "message": ""},
    "news": {"status": "pending", "message": ""}
}

print("🔑 API Keys Integration Test")
print("=" * 70)
print()

# ============================================================
# STEP 1: Check Environment Variables
# ============================================================

print("STEP 1: Checking Environment Variables")
print("-" * 70)

gemini_key = os.getenv("GEMINI_API_KEY")
weather_key = os.getenv("WEATHER_API_KEY")
news_key = os.getenv("NEWS_API_KEY")

if gemini_key:
    print(f"✅ GEMINI_API_KEY found: {gemini_key[:15]}... (length: {len(gemini_key)})")
else:
    print("❌ GEMINI_API_KEY not found in .env")
    results["gemini"]["status"] = "failed"
    results["gemini"]["message"] = "Key not found in .env"

if weather_key:
    print(f"✅ WEATHER_API_KEY found: {weather_key[:15]}... (length: {len(weather_key)})")
else:
    print("⚠️  WEATHER_API_KEY not found - will skip test")
    results["weather"]["status"] = "skipped"
    results["weather"]["message"] = "Key not configured"

if news_key:
    print(f"✅ NEWS_API_KEY found: {news_key[:15]}... (length: {len(news_key)})")
else:
    print("⚠️  NEWS_API_KEY not found - will skip test")
    results["news"]["status"] = "skipped"
    results["news"]["message"] = "Key not configured"

print()

# ============================================================
# STEP 2: Test Gemini API Key
# ============================================================

print("STEP 2: Testing Gemini API (Google Generative AI)")
print("-" * 70)

if not gemini_key:
    print("⚠️  Skipping - no API key provided")
    print()
else:
    try:
        import google.generativeai as genai
        
        print("Configuring Gemini with API key...")
        genai.configure(api_key=gemini_key)
        
        print("Creating model: models/gemini-2.5-flash...")
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
        print("Sending test request...")
        response = model.generate_content("Say 'Gemini API test successful!' in one sentence.")
        
        print(f"✅ GEMINI API WORKS!")
        print(f"   Response: {response.text[:100]}...")
        results["gemini"]["status"] = "success"
        results["gemini"]["message"] = "API working correctly"
        print()
        
    except Exception as e:
        print(f"❌ GEMINI API FAILED!")
        print(f"   Error: {e}")
        results["gemini"]["status"] = "failed"
        results["gemini"]["message"] = str(e)
        print()

# ============================================================
# STEP 3: Test Weather API Key (OpenWeatherMap)
# ============================================================

print("STEP 3: Testing Weather API (OpenWeatherMap)")
print("-" * 70)

if not weather_key:
    print("⚠️  Skipping - no API key provided")
    print()
else:
    try:
        import requests
        
        # Rome coordinates
        lat = 41.8003
        lon = 12.2389
        
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": weather_key,
            "units": "metric",
            "cnt": 8  # 1 day of forecasts
        }
        
        print(f"Calling OpenWeatherMap API for Rome...")
        print(f"URL: {url}")
        print(f"Params: lat={lat}, lon={lon}, units=metric")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check we got forecast data
            if "list" in data and len(data["list"]) > 0:
                first_forecast = data["list"][0]
                temp = first_forecast["main"]["temp"]
                condition = first_forecast["weather"][0]["main"]
                
                print(f"✅ WEATHER API WORKS!")
                print(f"   City: {data.get('city', {}).get('name', 'Rome')}")
                print(f"   Current forecast: {temp}°C, {condition}")
                print(f"   Received {len(data['list'])} forecast entries")
                results["weather"]["status"] = "success"
                results["weather"]["message"] = f"{temp}°C, {condition}"
                print()
            else:
                print(f"❌ WEATHER API FAILED!")
                print(f"   No forecast data in response")
                results["weather"]["status"] = "failed"
                results["weather"]["message"] = "No forecast data"
                print()
        
        elif response.status_code == 401:
            print(f"❌ WEATHER API KEY INVALID!")
            print(f"   Status: 401 Unauthorized")
            error_msg = response.json().get('message', 'Invalid API key')
            print(f"   Message: {error_msg}")
            print(f"   🔗 Get new key: https://openweathermap.org/api")
            results["weather"]["status"] = "invalid_key"
            results["weather"]["message"] = error_msg
            print()
        
        else:
            print(f"❌ WEATHER API FAILED!")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            results["weather"]["status"] = "failed"
            results["weather"]["message"] = f"HTTP {response.status_code}"
            print()
    
    except Exception as e:
        print(f"❌ WEATHER API FAILED!")
        print(f"   Error: {e}")
        results["weather"]["status"] = "failed"
        results["weather"]["message"] = str(e)
        print()

# ============================================================
# STEP 4: Test News API Key (NewsAPI.org)
# ============================================================

print("STEP 4: Testing News API (NewsAPI.org)")
print("-" * 70)

if not news_key:
    print("⚠️  Skipping - no API key provided")
    print()
else:
    try:
        import requests
        from datetime import datetime, timedelta
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "Rome",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 5,
            "apiKey": news_key,
            "from": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        }
        
        print(f"Calling NewsAPI for Rome news...")
        print(f"URL: {url}")
        print(f"Query: Rome, last 7 days, English")
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "ok" and "articles" in data:
                articles = data["articles"]
                
                print(f"✅ NEWS API WORKS!")
                print(f"   Total results: {data.get('totalResults', 0)}")
                print(f"   Articles received: {len(articles)}")
                
                if len(articles) > 0:
                    print(f"\n   Sample article:")
                    print(f"   Title: {articles[0].get('title', 'N/A')[:80]}...")
                    print(f"   Source: {articles[0].get('source', {}).get('name', 'N/A')}")
                
                results["news"]["status"] = "success"
                results["news"]["message"] = f"{len(articles)} articles found"
                print()
            else:
                print(f"❌ NEWS API FAILED!")
                print(f"   Status: {data.get('status')}")
                print(f"   Message: {data.get('message', 'Unknown error')}")
                results["news"]["status"] = "failed"
                results["news"]["message"] = data.get('message', 'Unknown error')
                print()
        
        elif response.status_code == 401:
            print(f"❌ NEWS API KEY INVALID!")
            print(f"   Status: 401 Unauthorized")
            error_msg = response.json().get('message', 'Invalid API key')
            print(f"   Message: {error_msg}")
            print(f"   🔗 Get new key: https://newsapi.org/")
            results["news"]["status"] = "invalid_key"
            results["news"]["message"] = error_msg
            print()
        
        elif response.status_code == 429:
            print(f"⚠️  NEWS API RATE LIMIT!")
            print(f"   Status: 429 Too Many Requests")
            print(f"   Free tier: 100 requests/day")
            print(f"   You may have hit the limit - try again tomorrow")
            results["news"]["status"] = "rate_limit"
            results["news"]["message"] = "Rate limit exceeded (100/day)"
            print()
        
        else:
            print(f"❌ NEWS API FAILED!")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            results["news"]["status"] = "failed"
            results["news"]["message"] = f"HTTP {response.status_code}"
            print()
    
    except Exception as e:
        print(f"❌ NEWS API FAILED!")
        print(f"   Error: {e}")
        results["news"]["status"] = "failed"
        results["news"]["message"] = str(e)
        print()

# ============================================================
# SUMMARY
# ============================================================

print("=" * 70)
print("📊 TEST RESULTS SUMMARY")
print("=" * 70)
print()

# Gemini
if results["gemini"]["status"] == "success":
    print("✅ Gemini API - WORKING")
elif results["gemini"]["status"] == "failed":
    print(f"❌ Gemini API - FAILED ({results['gemini']['message']})")
elif results["gemini"]["status"] == "skipped":
    print(f"⚠️  Gemini API - SKIPPED ({results['gemini']['message']})")

# Weather
if results["weather"]["status"] == "success":
    print(f"✅ Weather API - WORKING ({results['weather']['message']})")
elif results["weather"]["status"] == "invalid_key":
    print(f"❌ Weather API - INVALID KEY")
    print(f"   Action: Get new key at https://openweathermap.org/api")
elif results["weather"]["status"] == "failed":
    print(f"❌ Weather API - FAILED ({results['weather']['message']})")
elif results["weather"]["status"] == "skipped":
    print(f"⚠️  Weather API - SKIPPED ({results['weather']['message']})")

# News
if results["news"]["status"] == "success":
    print(f"✅ News API - WORKING ({results['news']['message']})")
elif results["news"]["status"] == "invalid_key":
    print(f"❌ News API - INVALID KEY")
    print(f"   Action: Get new key at https://newsapi.org/")
elif results["news"]["status"] == "rate_limit":
    print(f"⚠️  News API - RATE LIMITED (try tomorrow)")
elif results["news"]["status"] == "failed":
    print(f"❌ News API - FAILED ({results['news']['message']})")
elif results["news"]["status"] == "skipped":
    print(f"⚠️  News API - SKIPPED ({results['news']['message']})")

print()

# Overall status
working_count = sum(1 for r in results.values() if r["status"] == "success")
total_configured = sum(1 for r in results.values() if r["status"] != "skipped")

if working_count == total_configured and total_configured > 0:
    print("🎉 ALL CONFIGURED API KEYS ARE WORKING!")
    print()
    print("🚀 Ready to run adapter tests and start server!")
    exit_code = 0
elif working_count > 0:
    print(f"⚠️  PARTIAL SUCCESS: {working_count}/{total_configured} APIs working")
    print()
    print("💡 You can still run the server - failed APIs will use fallbacks:")
    print("   - Weather: will use mock data")
    print("   - News: will use Gemini-generated content")
    exit_code = 0
else:
    print("❌ NO APIs WORKING")
    print()
    print("⚠️  Action required: Fix API keys before continuing")
    exit_code = 1

print()
sys.exit(exit_code)

#!/bin/bash

# Install jq if needed
if ! command -v jq &> /dev/null; then
    echo "📦 Installing jq..."
    brew install jq
fi

BASE_URL="http://localhost:8000"

echo "🧪 Testing Inflight Experience API v2.0"
echo "========================================"
echo ""

# Health
echo "1️⃣  Health Check"
curl -s $BASE_URL/health | jq '.'
echo ""

# Passenger
echo "2️⃣  Passenger Info"
curl -s $BASE_URL/api/v1/passenger/P001 | jq '.'
echo ""

# Booking
echo "3️⃣  Booking Details (PNR: VY4K7M)"
curl -s $BASE_URL/api/v1/booking/VY4K7M | jq '.'
echo ""

# Flight (FIXED DATE FORMAT)
echo "4️⃣  Flight Details (VY71299 on 20260207)"
curl -s $BASE_URL/api/v1/flight/VY71299/20260207 | jq '.aircraft, .cockpit_crew'
echo ""

# Destination content (this will take 10-20 seconds)
echo "5️⃣  Destination Content (Rome - Spanish) - may take 10-20 sec..."
curl -s $BASE_URL/api/v1/destination/FCO/content/es | jq '.destination, .highlights[0].title, .restaurants[0].name'
echo ""

# Weather
echo "6️⃣  Weather (Rome - English)"
curl -s $BASE_URL/api/v1/destination/FCO/weather/en | jq '.'
echo ""

# News (this will take 10-15 seconds)
echo "7️⃣  News (Rome - Italian) - may take 10-15 sec..."
curl -s $BASE_URL/api/v1/destination/FCO/news/it | jq '.[0].title'
echo ""

echo "✅ Quick tests complete!"
echo ""
echo "💡 Try the BIG FLOW (will take 30-45 sec):"
echo "   curl $BASE_URL/api/v1/inflight-experience/VY4K7M/es | jq '.' > experience.json"

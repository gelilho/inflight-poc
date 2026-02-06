#!/bin/bash

# Install jq if needed
if ! command -v jq &> /dev/null; then
    echo "📦 Installing jq for pretty JSON output..."
    brew install jq
fi

BASE_URL="http://localhost:8000"

echo "🧪 Testing Inflight Experience API Endpoints"
echo "=============================================="
echo ""
echo "⚠️  Make sure server is running: ./run.sh"
echo ""

# Check if server is running
if ! curl -s $BASE_URL/health > /dev/null 2>&1; then
    echo "❌ Server is not running!"
    echo "   Start it with: ./run.sh"
    exit 1
fi

# Health check
echo "1️⃣  Health Check"
curl -s $BASE_URL/health | jq '.'
echo ""

# Booking
echo "2️⃣  Booking Details (PNR: VY4K7M)"
curl -s $BASE_URL/api/v1/booking/VY4K7M | jq '.'
echo ""

# Flight
echo "3️⃣  Flight Details (VY71299 on 20260207)"
curl -s $BASE_URL/api/v1/flight/VY71299/20260207 | jq '.aircraft, .cockpit_crew'
echo ""

# Destination content
echo "4️⃣  Destination Content (Rome - Spanish) - may take 10-20 sec..."
curl -s $BASE_URL/api/v1/destination/FCO/content/es | jq '.destination, .highlights[0].title, .restaurants[0].name'
echo ""

# Weather
echo "5️⃣  Weather (Rome - English)"
curl -s $BASE_URL/api/v1/destination/FCO/weather/en | jq '.'
echo ""

# News
echo "6️⃣  News (Rome - Italian) - may take 10-15 sec..."
curl -s $BASE_URL/api/v1/destination/FCO/news/it | jq '.[0].title'
echo ""

# Complete experience
echo "7️⃣  Complete Inflight Experience (Booking VY4K7M - Spanish)"
curl -s $BASE_URL/api/v1/inflight-experience/VY4K7M/es | jq '.booking.seat, .flight.aircraft.aircraft_name, .destination_content.destination.city'
echo ""

echo "✅ All endpoint tests complete!"
echo ""
echo "💡 Try full experience:"
echo "   curl $BASE_URL/api/v1/inflight-experience/VY4K7M/es | jq '.' > output.json"

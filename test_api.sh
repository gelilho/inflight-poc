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

# Flight
echo "4️⃣  Flight Details (VY71299 on 2026-02-07)"
curl -s $BASE_URL/api/v1/flight/VY71299/2026-02-07 | jq '.aircraft, .cockpit_crew'
echo ""

# Destination content
echo "5️⃣  Destination Content (Rome - Spanish)"
curl -s $BASE_URL/api/v1/destination/FCO/content/es | jq '.destination, .highlights[0].title, .restaurants[0].name'
echo ""

# Weather
echo "6️⃣  Weather (Rome - English)"
curl -s $BASE_URL/api/v1/destination/FCO/weather/en | jq '.'
echo ""

# News
echo "7️⃣  News (Rome - Italian)"
curl -s $BASE_URL/api/v1/destination/FCO/news/it | jq '.[0].title'
echo ""

# Complete experience
echo "8️⃣  Complete Inflight Experience (Booking VY4K7M - Spanish)"
curl -s $BASE_URL/api/v1/inflight-experience/VY4K7M/es | jq '.booking.seat, .flight.aircraft.aircraft_name, .destination_content.destination.city'
echo ""

echo "✅ All tests complete!"
echo ""
echo "💡 Try these commands:"
echo "   curl $BASE_URL/api/v1/booking/VY4K7M | jq '.'"
echo "   curl $BASE_URL/api/v1/flight/VY71299/2026-02-07 | jq '.'"
echo "   curl $BASE_URL/api/v1/destination/FCO/content/es | jq '.'"
echo "   curl $BASE_URL/api/v1/inflight-experience/VY4K7M/es | jq '.' > experience.json"

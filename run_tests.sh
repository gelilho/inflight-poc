#!/bin/bash

echo "🧪 Running All Tests"
echo "===================="
echo ""

# Activate venv
source venv/bin/activate

# Run adapter tests
echo "📦 Adapter Tests"
python tests/adapters/test_gemini_adapter.py
echo ""

python tests/adapters/test_weather_news_adapters.py
echo ""

# Run integration tests
echo "🔗 Integration Tests"
python tests/integration/test_api_keys_integration.py
echo ""

echo "✅ All tests complete!"

#!/bin/bash

echo "🧪 Running All Tests"
echo "===================="
echo ""

# Activate venv
source venv/bin/activate

# 1. Adapter Tests
echo "📦 Adapter Tests"
echo "----------------"
python tests/adapters/test_gemini_adapter.py
if [ $? -ne 0 ]; then
    echo "❌ Gemini adapter tests failed!"
    exit 1
fi
echo ""

python tests/adapters/test_weather_news_adapters.py
if [ $? -ne 0 ]; then
    echo "❌ Weather/News adapter tests failed!"
    exit 1
fi
echo ""

# 2. Integration Tests
echo "🔗 Integration Tests"
echo "--------------------"
python tests/integration/test_api_keys_integration.py
if [ $? -ne 0 ]; then
    echo "❌ API keys integration tests failed!"
    exit 1
fi
echo ""

# 3. API Endpoint Tests (requires server running)
echo "🌐 API Endpoint Tests"
echo "---------------------"
echo "Checking if server is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Server is running, testing endpoints..."
    ./tests/test_api_endpoints.sh
    if [ $? -ne 0 ]; then
        echo "❌ API endpoint tests failed!"
        exit 1
    fi
else
    echo "⚠️  Server not running, skipping endpoint tests"
    echo "   Start server with: ./run.sh"
fi
echo ""

echo "=" * 50
echo "✅ All tests passed!"
echo "=" * 50

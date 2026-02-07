#!/bin/bash

# Navigate to project root (one level up from scripts/)
cd "$(dirname "$0")/.."

echo "Running All Tests"
echo "=================="
echo ""

# Unit + Integration tests (no real API calls, fast)
echo "Unit + Integration tests (mocked APIs)..."
echo "------------------------------------------"
python -m pytest -m "not live" --tb=short
UNIT_RESULT=$?
echo ""

if [ $UNIT_RESULT -ne 0 ]; then
    echo "Unit/Integration tests FAILED!"
    exit 1
fi

# Ask if user wants to run live API tests
echo "Run live API tests? (real calls to Gemini/Weather/News)"
echo "  pytest -m live"
echo ""
echo "All mocked tests passed!"

#!/bin/bash

echo "🧹 Cleaning Up Project"
echo "======================"
echo ""

REMOVED=0

safe_remove() {
    if [ -e "$1" ]; then
        echo "Removing: $1"
        rm -rf "$1"
        REMOVED=$((REMOVED + 1))
    fi
}

# Remove old test files from root
echo "1️⃣  Removing old test files from root..."
safe_remove "test_api.sh"  # Moved to tests/
safe_remove "test_gemini.py"
safe_remove "test_gemini_adapter.py"
safe_remove "test_weather_news_adapters.py"
safe_remove "test_api_keys_integration.py"
safe_remove "check_api_keys.py"
safe_remove "test_model.py"
safe_remove "test_working_model.py"
safe_remove "list_models.py"

# Remove output files
echo "2️⃣  Removing output files..."
safe_remove "demo_complete.json"
safe_remove "demo_full.json"
safe_remove "experience.json"
safe_remove "output.json"

# Remove Python cache
echo "3️⃣  Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -exec rm -f {} + 2>/dev/null

# Remove pytest cache
echo "4️⃣  Removing pytest cache..."
safe_remove ".pytest_cache"

# Remove Mac files
echo "5️⃣  Removing Mac system files..."
find . -name ".DS_Store" -exec rm -f {} + 2>/dev/null

echo ""
echo "✅ Cleanup complete! Removed $REMOVED items."

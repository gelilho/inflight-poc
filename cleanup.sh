#!/bin/bash

echo "🧹 Cleaning Up Project"
echo "======================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track what we're removing
REMOVED=0

# Function to safely remove
safe_remove() {
    if [ -e "$1" ]; then
        echo -e "${YELLOW}Removing:${NC} $1"
        rm -rf "$1"
        REMOVED=$((REMOVED + 1))
    fi
}

# 1. Remove old test files from root (now in tests/)
echo "1️⃣  Checking for old test files in root..."
safe_remove "test_gemini.py"
safe_remove "test_gemini_adapter.py"
safe_remove "test_weather_news_adapters.py"
safe_remove "test_api_keys_integration.py"
safe_remove "check_api_keys.py"
safe_remove "test_model.py"
safe_remove "test_working_model.py"
safe_remove "list_models.py"
echo ""

# 2. Remove demo/output JSON files
echo "2️⃣  Checking for demo/output JSON files..."
safe_remove "demo_complete.json"
safe_remove "demo_full.json"
safe_remove "demo_for_mwc.json"
safe_remove "demo_pretty.json"
safe_remove "experience.json"
safe_remove "full_experience.json"
safe_remove "inflight_experience_demo.json"
echo ""

# 3. Remove Python cache
echo "3️⃣  Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -exec rm -f {} + 2>/dev/null
find . -type f -name "*.pyo" -exec rm -f {} + 2>/dev/null
find . -type f -name "*.pyd" -exec rm -f {} + 2>/dev/null
echo "   ✅ Python cache cleaned"
echo ""

# 4. Remove backup files
echo "4️⃣  Checking for backup files..."
safe_remove "*.backup"
safe_remove "*.bak"
find . -maxdepth 2 -name "*~" -exec rm -f {} + 2>/dev/null
echo ""

# 5. Remove pytest cache
echo "5️⃣  Removing pytest cache..."
safe_remove ".pytest_cache"
safe_remove ".coverage"
safe_remove "htmlcov"
echo ""

# 6. Remove log files
echo "6️⃣  Checking for log files..."
find . -maxdepth 2 -name "*.log" -exec rm -f {} + 2>/dev/null
echo "   ✅ Log files cleaned"
echo ""

# 7. Remove DS_Store (Mac)
echo "7️⃣  Removing Mac system files..."
find . -name ".DS_Store" -exec rm -f {} + 2>/dev/null
echo "   ✅ .DS_Store files cleaned"
echo ""

# 8. Check for duplicate/old config files
echo "8️⃣  Checking for duplicate config files..."
if [ -f "config/environments/.env.local" ]; then
    echo -e "${YELLOW}Found:${NC} config/environments/.env.local (might be duplicate of .env)"
fi
echo ""

# Summary
echo "=" * 50
if [ $REMOVED -gt 0 ]; then
    echo -e "${GREEN}✅ Cleanup complete! Removed $REMOVED items.${NC}"
else
    echo -e "${GREEN}✅ Project already clean! Nothing to remove.${NC}"
fi
echo ""
echo "📊 Current project status:"
echo "   Files in root: $(ls -1 | wc -l)"
echo "   Python cache dirs: $(find . -type d -name "__pycache__" 2>/dev/null | wc -l)"
echo "   Test files: $(find tests/ -name "test_*.py" 2>/dev/null | wc -l)"
echo ""

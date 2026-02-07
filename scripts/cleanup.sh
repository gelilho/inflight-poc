#!/bin/bash

# Navigate to project root (one level up from scripts/)
cd "$(dirname "$0")/.."

echo "Cleaning Up Project"
echo "===================="
echo ""

REMOVED=0

safe_remove() {
    if [ -e "$1" ]; then
        echo "  Removing: $1"
        rm -rf "$1"
        REMOVED=$((REMOVED + 1))
    fi
}

# 1. Remove misplaced test files from root
echo "1. Removing misplaced test files from root..."
for f in test_*.py; do
    [ -e "$f" ] && safe_remove "$f"
done

# 2. Remove output files from root
echo "2. Removing output JSON files..."
for f in *.json; do
    [ -e "$f" ] && safe_remove "$f"
done

# 3. Remove Python cache
echo "3. Removing Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -exec rm -f {} + 2>/dev/null

# 4. Remove pytest cache
echo "4. Removing pytest cache..."
safe_remove ".pytest_cache"

# 5. Remove Mac system files
echo "5. Removing .DS_Store files..."
find . -name ".DS_Store" -exec rm -f {} + 2>/dev/null

# 6. Remove backup files
echo "6. Removing backup files..."
find . -maxdepth 2 \( -name "*.backup" -o -name "*.bak" -o -name "*~" \) -exec rm -f {} + 2>/dev/null

echo ""
echo "Cleanup complete! Removed $REMOVED items."

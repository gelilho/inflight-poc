#!/bin/bash

echo "🏥 Project Health Check"
echo "======================="
echo ""

# Check for issues
ISSUES=0

# 1. Check for test files in root
echo "1️⃣  Checking for misplaced test files..."
TEST_FILES=$(find . -maxdepth 1 -name "test_*.py" 2>/dev/null | wc -l)
if [ $TEST_FILES -gt 0 ]; then
    echo "   ⚠️  Found $TEST_FILES test files in root (should be in tests/)"
    find . -maxdepth 1 -name "test_*.py"
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ No test files in root"
fi
echo ""

# 2. Check for JSON output files
echo "2️⃣  Checking for output JSON files..."
JSON_FILES=$(find . -maxdepth 1 -name "*.json" 2>/dev/null | wc -l)
if [ $JSON_FILES -gt 0 ]; then
    echo "   ⚠️  Found $JSON_FILES JSON files in root"
    find . -maxdepth 1 -name "*.json"
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ No output files in root"
fi
echo ""

# 3. Check for Python cache
echo "3️⃣  Checking for Python cache..."
CACHE_DIRS=$(find . -type d -name "__pycache__" 2>/dev/null | wc -l)
if [ $CACHE_DIRS -gt 5 ]; then
    echo "   ⚠️  Found $CACHE_DIRS __pycache__ directories"
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ Python cache minimal"
fi
echo ""

# 4. Check .env is not in git
echo "4️⃣  Checking .env is not tracked..."
if git ls-files --error-unmatch .env &>/dev/null; then
    echo "   ❌ CRITICAL: .env is tracked by git!"
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ .env is not tracked"
fi
echo ""

# 5. Check project structure
echo "5️⃣  Checking project structure..."
REQUIRED_DIRS=("app" "config" "data" "tests")
for dir in "${REQUIRED_DIRS[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "   ❌ Missing required directory: $dir"
        ISSUES=$((ISSUES + 1))
    fi
done
echo "   ✅ All required directories exist"
echo ""

# 6. Check for backup files
echo "6️⃣  Checking for backup files..."
BACKUP_FILES=$(find . -maxdepth 2 \( -name "*.backup" -o -name "*.bak" -o -name "*~" \) 2>/dev/null | wc -l)
if [ $BACKUP_FILES -gt 0 ]; then
    echo "   ⚠️  Found $BACKUP_FILES backup files"
    ISSUES=$((ISSUES + 1))
else
    echo "   ✅ No backup files"
fi
echo ""

# Summary
echo "======================="
if [ $ISSUES -eq 0 ]; then
    echo "✅ Project is clean and healthy!"
else
    echo "⚠️  Found $ISSUES issues"
    echo ""
    echo "Run './cleanup.sh' to fix automatically."
fi
echo ""

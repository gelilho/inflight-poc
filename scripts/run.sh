#!/bin/bash

# Navigate to project root (one level up from scripts/)
cd "$(dirname "$0")/.."

echo "Starting Inflight Experience API..."
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

#!/bin/bash

echo "🚀 Starting Inflight Experience API..."
echo ""
echo "Environment: $(cat .env | grep ENVIRONMENT | cut -d'=' -f2)"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

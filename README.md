
## Running Tests

### All Tests (mocked, no API calls)
```bash
scripts/run_tests.sh
```

### Specific Test Suites

**Unit Tests:**
```bash
python -m pytest tests/unit/ -v
```

**Integration Tests (mocked API endpoints):**
```bash
python -m pytest tests/integration/ -v
```

**Live API Tests (real calls to Gemini/Weather/News):**
```bash
python -m pytest -m live -v
```

### Test Structure
```
tests/
├── unit/                  # Unit tests (mocked adapters)
│   ├── test_csv_loader.py
│   ├── test_gemini_adapter.py
│   ├── test_news_filtering.py
│   ├── test_schemas.py
│   └── test_services.py
├── integration/           # Integration tests
│   ├── test_api_endpoints.py
│   └── test_api_keys_integration.py
└── test_api_endpoints.sh  # cURL-based endpoint smoke tests
```


## 🧪 Running Tests

### All Tests
```bash
./run_tests.sh
```

### Specific Test Suites

**Adapter Tests:**
```bash
python tests/adapters/test_gemini_adapter.py
python tests/adapters/test_weather_news_adapters.py
```

**Integration Tests:**
```bash
python tests/integration/test_api_keys_integration.py
```

### Test Structure
```
tests/
├── adapters/          # Adapter-specific tests
│   ├── test_gemini_adapter.py
│   └── test_weather_news_adapters.py
├── integration/       # API key integration tests
│   └── test_api_keys_integration.py
└── unit/             # Unit tests (future)
```

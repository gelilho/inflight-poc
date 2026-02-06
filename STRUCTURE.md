# 📂 Project Structure
```
inflight-poc/
│
├── app/                          # Main application code
│   ├── adapters/                 # External API integrations
│   │   ├── gemini_adapter.py     # Google Gemini LLM
│   │   ├── weather_adapter.py    # OpenWeatherMap
│   │   └── news_adapter.py       # NewsAPI.org
│   │
│   ├── api/                      # FastAPI endpoints
│   │   └── endpoints.py          # All REST endpoints
│   │
│   ├── models/                   # Data schemas
│   │   └── schemas.py            # Pydantic models
│   │
│   ├── prompts/                  # LLM prompts (centralized)
│   │   ├── base_prompts.py       # Base rules & config
│   │   ├── destination_prompts.py # Content generation
│   │   └── translation_prompts.py # Translation
│   │
│   ├── services/                 # Business logic
│   │   ├── passenger_service.py  # Passenger operations
│   │   ├── flight_service.py     # Flight operations
│   │   ├── destination_service.py # Destination content
│   │   └── inflight_service.py   # Orchestration (BIG FLOW)
│   │
│   └── main.py                   # FastAPI app entry point
│
├── config/                       # Configuration
│   ├── settings.py               # Pydantic settings
│   ├── constants.py              # Fixed values
│   └── environments/
│       └── .env.template         # Environment template
│
├── data/                         # Data layer
│   ├── loaders/
│   │   └── csv_loader.py         # CSV data loader
│   └── mock/                     # Mock data (CSV)
│       ├── bookings.csv          # Booking data
│       ├── flights.csv           # Flight data
│       ├── passengers.csv        # Passenger data
│       └── destinations.csv      # Destination data
│
├── tests/                        # ALL TESTS HERE
│   ├── adapters/                 # Adapter tests
│   │   ├── test_gemini_adapter.py
│   │   └── test_weather_news_adapters.py
│   ├── integration/              # Integration tests
│   │   └── test_api_keys_integration.py
│   ├── unit/                     # Unit tests (future)
│   └── test_api_endpoints.sh    # API endpoint tests
│
├── .env                          # Environment variables (NOT in git)
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
├── STRUCTURE.md                  # This file
├── STATUS.md                     # Current project status
├── requirements.txt              # Python dependencies
├── pytest.ini                    # Test configuration
├── run.sh                        # Start server script
├── run_tests.sh                  # Run all tests
├── cleanup.sh                    # Cleanup temporary files
└── health_check.sh              # Project health check
```

## Key Changes

✅ **ALL tests now in `tests/` directory**
- Unit tests: `tests/unit/`
- Integration tests: `tests/integration/`
- Adapter tests: `tests/adapters/`
- API endpoint tests: `tests/test_api_endpoints.sh`

✅ **Root directory is clean**
- Only essential scripts: `run.sh`, `run_tests.sh`, `cleanup.sh`, `health_check.sh`
- No test files
- No output files
- Professional structure

## Running Tests
```bash
# All tests (including API endpoints if server running)
./run_tests.sh

# Individual test suites
python tests/adapters/test_gemini_adapter.py
python tests/integration/test_api_keys_integration.py
./tests/test_api_endpoints.sh  # Requires server running
```

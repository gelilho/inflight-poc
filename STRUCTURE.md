# Project Structure
```
inflight-poc/
│
├── app/                          # Main application code
│   ├── adapters/                 # AI engine
│   │   ├── gemini_adapter.py     # Google Gemini 2.5 Flash (ALL content)
│   │   ├── weather_adapter.py    # (legacy — not used, Gemini generates weather)
│   │   └── news_adapter.py       # (legacy — not used, Gemini generates news)
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
│   │   └── inflight_service.py   # Orchestration (full experience)
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
│   ├── unit/                     # Unit tests (mocked adapters)
│   │   ├── test_csv_loader.py
│   │   ├── test_gemini_adapter.py
│   │   ├── test_news_filtering.py
│   │   ├── test_schemas.py
│   │   └── test_services.py
│   ├── integration/              # Integration tests
│   │   ├── test_api_endpoints.py
│   │   └── test_api_keys_integration.py
│   └── test_api_endpoints.sh     # cURL-based endpoint smoke tests
│
├── scripts/                      # Utility scripts
│   ├── run.sh                    # Start server
│   ├── run_tests.sh              # Run all tests
│   ├── cleanup.sh                # Cleanup temp files
│   └── health_check.sh           # Project health check
│
├── business-docs/                # Business documentation
│   ├── ONE_PAGER.md
│   ├── DECK.md
│   ├── TRIGGER_FLOW.md
│   ├── PITCH_SCRIPT.md
│   ├── TECHNICAL_ARCHITECTURE.md
│   └── KPIs_AND_METRICS.md
│
├── .env                          # Environment variables (NOT in git)
├── .gitignore                    # Git ignore rules
├── README.md                     # Project documentation
├── STRUCTURE.md                  # This file
├── STATUS.md                     # Current project status
├── requirements.txt              # Python dependencies
└── pytest.ini                    # Test configuration
```

## Running Tests
```bash
# All mocked tests (unit + integration, no real API calls)
scripts/run_tests.sh

# Individual test suites
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v

# Live API tests (real calls to Gemini)
python -m pytest -m live -v

# cURL endpoint smoke tests (requires server running)
bash tests/test_api_endpoints.sh
```

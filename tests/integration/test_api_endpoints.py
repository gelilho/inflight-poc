"""Integration tests for API endpoints using FastAPI TestClient.

These test the full HTTP request/response cycle without a running server.
External APIs (Gemini, Weather, News) are mocked so tests are fast and free.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


# ============================================================
# HEALTH & ROOT ENDPOINTS
# ============================================================

class TestHealthEndpoints:

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "supported_languages" in data

    def test_root_returns_api_info(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "endpoints" in data
        assert "supported_languages" in data


# ============================================================
# PASSENGER ENDPOINTS
# ============================================================

class TestPassengerEndpoints:

    def test_get_passenger_success(self, client):
        response = client.get("/api/v1/passenger/P001")
        assert response.status_code == 200
        data = response.json()
        assert data["first_name"] == "Angel"
        assert data["last_name"] == "Lopez"

    def test_get_passenger_not_found(self, client):
        response = client.get("/api/v1/passenger/P999")
        assert response.status_code == 404

    def test_get_passenger_bookings_success(self, client):
        response = client.get("/api/v1/passenger/P001/bookings")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_passenger_bookings_not_found(self, client):
        response = client.get("/api/v1/passenger/P999/bookings")
        assert response.status_code == 404


# ============================================================
# BOOKING ENDPOINT
# ============================================================

class TestBookingEndpoint:

    def test_get_booking_success(self, client):
        response = client.get("/api/v1/booking/VY4K7M")
        assert response.status_code == 200
        data = response.json()
        assert data["booking_number"] == "VY4K7M"
        assert data["seat"] == "14D"
        assert data["origin"] == "BCN"
        assert data["destination"] == "FCO"

    def test_get_booking_not_found(self, client):
        response = client.get("/api/v1/booking/XXXXXX")
        assert response.status_code == 404


# ============================================================
# FLIGHT ENDPOINT
# ============================================================

class TestFlightEndpoint:

    def test_get_flight_success(self, client):
        response = client.get("/api/v1/flight/VY71299/20260207")
        assert response.status_code == 200
        data = response.json()
        assert data["flight_number"] == "VY71299"
        assert data["aircraft"]["model"] == "Airbus A320-200"
        assert data["cockpit_crew"]["captain"]["first_name"] == "Laura"
        assert len(data["cabin_crew"]) == 3

    def test_get_flight_not_found(self, client):
        response = client.get("/api/v1/flight/XX9999/20260207")
        assert response.status_code == 404

    def test_get_flight_wrong_date(self, client):
        response = client.get("/api/v1/flight/VY71299/20991231")
        assert response.status_code == 404


# ============================================================
# DESTINATION ENDPOINTS (mocked Gemini)
# ============================================================

class TestDestinationEndpoints:

    def test_destination_content_unsupported_language(self, client):
        response = client.get("/api/v1/destination/FCO/content/xx")
        assert response.status_code == 400
        assert "Unsupported language" in response.json()["detail"]

    def test_weather_unsupported_language(self, client):
        response = client.get("/api/v1/destination/FCO/weather/xx")
        assert response.status_code == 400

    def test_news_unsupported_language(self, client):
        response = client.get("/api/v1/destination/FCO/news/xx")
        assert response.status_code == 400

    def test_weather_returns_3_days(self, client):
        """Weather uses mock fallback when API key is invalid — still returns 3 days"""
        response = client.get("/api/v1/destination/FCO/weather/en")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert "date" in data[0]
        assert "condition" in data[0]
        assert "min_temperature_c" in data[0]
        assert "max_temperature_c" in data[0]


# ============================================================
# INFLIGHT EXPERIENCE (BIG FLOW) — Language validation only
# ============================================================

class TestInflightExperienceEndpoint:

    def test_unsupported_language_returns_400(self, client):
        response = client.get("/api/v1/inflight-experience/VY4K7M/xx")
        assert response.status_code == 400

    def test_nonexistent_booking_returns_404(self, client):
        response = client.get("/api/v1/inflight-experience/XXXXXX/en")
        assert response.status_code == 404

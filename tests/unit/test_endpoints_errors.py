"""Unit tests for API endpoint exception handling (500 errors).

Tests the error paths that are NOT covered by the integration tests,
which only test happy paths and 404s. These tests verify that unexpected
exceptions are caught and returned as proper 500 responses.
"""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)


# ============================================================
# 500 ERROR HANDLING — PASSENGER ENDPOINTS
# ============================================================

class TestPassengerEndpointErrors:

    @patch("app.api.endpoints.passenger_service")
    def test_get_passenger_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_passenger.side_effect = RuntimeError("DB connection lost")
        response = client.get("/api/v1/passenger/P001")
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]

    @patch("app.api.endpoints.passenger_service")
    def test_get_bookings_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_passenger_bookings.side_effect = RuntimeError("DB connection lost")
        response = client.get("/api/v1/passenger/P001/bookings")
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]


# ============================================================
# 500 ERROR HANDLING — BOOKING ENDPOINT
# ============================================================

class TestBookingEndpointErrors:

    @patch("app.api.endpoints.passenger_service")
    def test_get_booking_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_booking.side_effect = RuntimeError("Unexpected failure")
        response = client.get("/api/v1/booking/VY4K7M")
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]


# ============================================================
# 500 ERROR HANDLING — FLIGHT ENDPOINT
# ============================================================

class TestFlightEndpointErrors:

    @patch("app.api.endpoints.flight_service")
    def test_get_flight_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_flight.side_effect = RuntimeError("CSV read failure")
        response = client.get("/api/v1/flight/VY71299/20260207")
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]


# ============================================================
# 500 ERROR HANDLING — DESTINATION ENDPOINTS
# ============================================================

class TestDestinationEndpointErrors:

    @patch("app.api.endpoints.destination_service")
    def test_destination_content_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_destination_content.side_effect = RuntimeError("Gemini crash")
        response = client.get("/api/v1/destination/FCO/content/en")
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]

    @patch("app.api.endpoints.destination_service")
    def test_weather_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_weather.side_effect = RuntimeError("Gemini crash")
        response = client.get("/api/v1/destination/FCO/weather/en")
        assert response.status_code == 500
        assert "Failed to fetch weather" in response.json()["detail"]

    @patch("app.api.endpoints.destination_service")
    def test_news_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_news.side_effect = RuntimeError("Gemini crash")
        response = client.get("/api/v1/destination/FCO/news/en")
        assert response.status_code == 500
        assert "Failed to fetch news" in response.json()["detail"]


# ============================================================
# 500 ERROR HANDLING — INFLIGHT EXPERIENCE
# ============================================================

class TestInflightExperienceEndpointErrors:

    @patch("app.api.endpoints.inflight_service")
    def test_inflight_500_on_unexpected_error(self, mock_svc, client):
        mock_svc.get_inflight_experience.side_effect = RuntimeError("Orchestration failed")
        response = client.get("/api/v1/inflight-experience/VY4K7M/en")
        assert response.status_code == 500
        assert "Internal server error" in response.json()["detail"]

"""Unit tests for services with mocked adapters — no real API calls"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.passenger_service import PassengerService
from app.services.flight_service import FlightService
from app.services.destination_service import DestinationService
from app.models.schemas import (
    Passenger, Booking, Flight, Aircraft, CockpitCrew, CrewMember,
    CabinCrewMember, Destination, EmergencyContacts
)


# ============================================================
# FIXTURES
# ============================================================

def _make_passenger():
    return Passenger(
        user_id="P001",
        first_name="Angel",
        last_name="Lopez",
        frequent_flyer_number="VY123456789",
        preferred_language="es"
    )


def _make_booking():
    return Booking(
        booking_number="VY4K7M",
        user_id="P001",
        flight_number="VY71299",
        flight_date="20260207",
        seat="14D",
        origin="BCN",
        origin_airport_name="Barcelona El Prat",
        destination="FCO",
        destination_airport_name="Rome Fiumicino",
        baggage_claim_belt="Carousel 5",
        booking_class="Economy",
        status="checked_in"
    )


def _make_flight():
    return Flight(
        flight_number="VY71299",
        flight_date="20260207",
        departure_time="14:30",
        arrival_time="16:15",
        origin="BCN",
        destination="FCO",
        aircraft=Aircraft(
            model="Airbus A320-200",
            registration="EC-MXY",
            age_years=9,
            aircraft_name="Spirit of Barcelona"
        ),
        cockpit_crew=CockpitCrew(
            captain=CrewMember(first_name="Laura", last_name="Rossi"),
            first_officer=CrewMember(first_name="Marco", last_name="Bianchi")
        ),
        cabin_crew=[
            CabinCrewMember(first_name="Sofia"),
            CabinCrewMember(first_name="Elena"),
            CabinCrewMember(first_name="Paolo"),
        ],
        average_duration_minutes=105,
        departure_gate="B23",
        baggage_claim_belt="Carousel 5"
    )


# ============================================================
# PASSENGER SERVICE
# ============================================================

class TestPassengerService:

    def setup_method(self):
        self.service = PassengerService()

    @patch("app.services.passenger_service.csv_loader")
    def test_get_passenger_returns_passenger(self, mock_loader):
        mock_loader.get_passenger.return_value = _make_passenger()
        result = self.service.get_passenger("P001")
        assert result.first_name == "Angel"
        mock_loader.get_passenger.assert_called_once_with("P001")

    @patch("app.services.passenger_service.csv_loader")
    def test_get_passenger_not_found_raises(self, mock_loader):
        mock_loader.get_passenger.return_value = None
        with pytest.raises(ValueError, match="Passenger not found"):
            self.service.get_passenger("P999")

    @patch("app.services.passenger_service.csv_loader")
    def test_get_booking_returns_booking(self, mock_loader):
        mock_loader.get_booking.return_value = _make_booking()
        result = self.service.get_booking("VY4K7M")
        assert result.seat == "14D"

    @patch("app.services.passenger_service.csv_loader")
    def test_get_booking_not_found_raises(self, mock_loader):
        mock_loader.get_booking.return_value = None
        with pytest.raises(ValueError, match="Booking not found"):
            self.service.get_booking("XXXXXX")

    @patch("app.services.passenger_service.csv_loader")
    def test_get_passenger_bookings_verifies_passenger_exists(self, mock_loader):
        mock_loader.get_passenger.return_value = None
        with pytest.raises(ValueError, match="Passenger not found"):
            self.service.get_passenger_bookings("P999")

    @patch("app.services.passenger_service.csv_loader")
    def test_get_passenger_bookings_returns_list(self, mock_loader):
        mock_loader.get_passenger.return_value = _make_passenger()
        mock_loader.get_bookings_by_user.return_value = [_make_booking()]
        result = self.service.get_passenger_bookings("P001")
        assert len(result) == 1
        assert result[0].booking_number == "VY4K7M"


# ============================================================
# FLIGHT SERVICE
# ============================================================

class TestFlightService:

    def setup_method(self):
        self.service = FlightService()

    @patch("app.services.flight_service.csv_loader")
    def test_get_flight_returns_flight(self, mock_loader):
        mock_loader.get_flight.return_value = _make_flight()
        result = self.service.get_flight("VY71299", "20260207")
        assert result.flight_number == "VY71299"
        assert result.aircraft.model == "Airbus A320-200"

    @patch("app.services.flight_service.csv_loader")
    def test_get_flight_not_found_raises(self, mock_loader):
        mock_loader.get_flight.return_value = None
        with pytest.raises(ValueError, match="Flight not found"):
            self.service.get_flight("XX9999", "20260207")


# ============================================================
# DESTINATION SERVICE
# ============================================================

class TestDestinationService:

    def setup_method(self):
        self.service = DestinationService()

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_get_destination_content_in_english(self, mock_loader, mock_gemini):
        """English content should NOT trigger translation"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39 06 3570", airport_info="+39 06 65951",
                vueling_contact="+34 931 518 158"
            )
        }
        mock_gemini.generate_highlights.return_value = [
            {"id": f"H00{i}", "title": f"Place {i}",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 6)
        ]
        mock_gemini.generate_restaurants.return_value = [
            {"name": f"Restaurant {i}", "cuisine": "Italian",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 4)
        ]
        mock_gemini.generate_airport_transport.return_value = [
            {"mode": "train", "estimated_duration_minutes": 30, "notes": "Fast"}
        ]

        result = self.service.get_destination_content("FCO", "en")

        assert result.destination.city == "Rome"
        assert len(result.highlights) == 5
        assert len(result.restaurants) == 3
        mock_gemini.translate_content.assert_not_called()

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_get_destination_content_non_english_passes_language_to_gemini(self, mock_loader, mock_gemini):
        """Non-English should pass language directly to Gemini (no separate translation)"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_highlights.return_value = [
            {"id": f"H00{i}", "title": f"Lugar {i}",
             "brief_description": "Breve", "long_description": "Largo"}
            for i in range(1, 6)
        ]
        mock_gemini.generate_restaurants.return_value = [
            {"name": f"R {i}", "cuisine": "Italiano",
             "brief_description": "Breve", "long_description": "Largo"}
            for i in range(1, 4)
        ]
        mock_gemini.generate_airport_transport.return_value = [
            {"mode": "train", "estimated_duration_minutes": 30, "notes": "Rapido"}
        ]

        result = self.service.get_destination_content("FCO", "es")
        # Verify language was passed directly to generate methods
        mock_gemini.generate_highlights.assert_called_once_with("Rome", "Italy", "es")
        mock_gemini.generate_restaurants.assert_called_once_with("Rome", "Italy", "es")
        mock_gemini.generate_airport_transport.assert_called_once_with("Rome", "FCO", "es")
        # No translation call needed
        mock_gemini.translate_content.assert_not_called()

    @patch("app.services.destination_service.csv_loader")
    def test_get_destination_content_unknown_airport_raises(self, mock_loader):
        mock_loader.get_destination_info.return_value = None
        with pytest.raises(ValueError, match="Destination not found"):
            self.service.get_destination_content("XXX", "en")

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_get_weather_returns_forecasts(self, mock_loader, mock_gemini):
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_weather.return_value = [
            {"date": "2026-02-07", "condition": "Sunny",
             "min_temperature_c": 12.0, "max_temperature_c": 22.0},
            {"date": "2026-02-08", "condition": "Cloudy",
             "min_temperature_c": 10.0, "max_temperature_c": 18.0},
            {"date": "2026-02-09", "condition": "Clear",
             "min_temperature_c": 11.0, "max_temperature_c": 20.0},
        ]
        result = self.service.get_weather("FCO", "en")
        assert len(result) == 3
        assert result[0].condition == "Sunny"
        mock_gemini.generate_weather.assert_called_once_with("Rome", "en")

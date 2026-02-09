"""Unit tests for services with mocked adapters — no real API calls"""

import pytest
from unittest.mock import patch, MagicMock
from app.services.passenger_service import PassengerService
from app.services.flight_service import FlightService
from app.services.destination_service import DestinationService
from app.services.inflight_service import InflightService
from app.models.schemas import (
    Passenger, Booking, Flight, Aircraft, CockpitCrew, CrewMember,
    CabinCrewMember, Destination, EmergencyContacts, DestinationContent,
    Highlight, Restaurant, AirportTransport, TransportOption,
    WeatherForecast, LocalNews
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


# ============================================================
# DESTINATION SERVICE — CACHE BEHAVIOR
# ============================================================

class TestDestinationServiceCache:
    """Test that in-memory cache returns data without regeneration"""

    def setup_method(self):
        self.service = DestinationService()

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_content_cache_hit_skips_gemini(self, mock_loader, mock_gemini):
        """Second call should return cached content — Gemini NOT called twice"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_highlights.return_value = [
            {"id": f"H00{i}", "title": f"Place {i}",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 6)
        ]
        mock_gemini.generate_restaurants.return_value = [
            {"name": f"R{i}", "cuisine": "Italian",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 4)
        ]
        mock_gemini.generate_airport_transport.return_value = [
            {"mode": "train", "estimated_duration_minutes": 30, "notes": "Fast"}
        ]

        # First call: generates content
        result1 = self.service.get_destination_content("FCO", "en")
        # Second call: should use cache
        result2 = self.service.get_destination_content("FCO", "en")

        assert result1.destination.city == result2.destination.city
        # Gemini should only be called ONCE (first call)
        assert mock_gemini.generate_highlights.call_count == 1

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_weather_cache_hit_skips_gemini(self, mock_loader, mock_gemini):
        """Second weather call should use cache"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_weather.return_value = [
            {"date": "2026-02-09", "condition": "Sunny",
             "min_temperature_c": 10.0, "max_temperature_c": 20.0}
        ]

        self.service.get_weather("FCO", "en")
        self.service.get_weather("FCO", "en")

        assert mock_gemini.generate_weather.call_count == 1

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_news_cache_hit_skips_gemini(self, mock_loader, mock_gemini):
        """Second news call should use cache"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_news.return_value = [
            {"title": "Festival", "brief_description": "Brief",
             "long_description": "Long", "category": "culture"}
        ]

        self.service.get_news("FCO", "en")
        self.service.get_news("FCO", "en")

        assert mock_gemini.generate_news.call_count == 1

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_different_languages_are_cached_separately(self, mock_loader, mock_gemini):
        """FCO/en and FCO/es should be separate cache entries"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_weather.return_value = [
            {"date": "2026-02-09", "condition": "Sunny",
             "min_temperature_c": 10.0, "max_temperature_c": 20.0}
        ]

        self.service.get_weather("FCO", "en")
        self.service.get_weather("FCO", "es")

        # Two different language calls = two Gemini calls
        assert mock_gemini.generate_weather.call_count == 2


# ============================================================
# DESTINATION SERVICE — FALLBACKS
# ============================================================

class TestDestinationServiceFallbacks:
    """Test fallback behavior when Gemini fails"""

    def setup_method(self):
        self.service = DestinationService()

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_highlights_fallback_on_gemini_failure(self, mock_loader, mock_gemini):
        """When highlights fail, fallback content is used"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_highlights.side_effect = Exception("Gemini timeout")
        mock_gemini.generate_restaurants.return_value = [
            {"name": f"R{i}", "cuisine": "Italian",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 4)
        ]
        mock_gemini.generate_airport_transport.return_value = [
            {"mode": "taxi", "estimated_duration_minutes": 30, "notes": "Available"}
        ]

        result = self.service.get_destination_content("FCO", "en")
        assert len(result.highlights) == 5
        assert "Rome" in result.highlights[0].title

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_restaurants_fallback_on_gemini_failure(self, mock_loader, mock_gemini):
        """When restaurants fail, fallback content is used"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_highlights.return_value = [
            {"id": f"H00{i}", "title": f"Place {i}",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 6)
        ]
        mock_gemini.generate_restaurants.side_effect = Exception("Gemini timeout")
        mock_gemini.generate_airport_transport.return_value = [
            {"mode": "taxi", "estimated_duration_minutes": 30, "notes": "Available"}
        ]

        result = self.service.get_destination_content("FCO", "en")
        assert len(result.restaurants) == 3
        assert "Rome" in result.restaurants[0].name

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_transport_fallback_on_gemini_failure(self, mock_loader, mock_gemini):
        """When transport fails, fallback taxi option is used"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_highlights.return_value = [
            {"id": f"H00{i}", "title": f"Place {i}",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 6)
        ]
        mock_gemini.generate_restaurants.return_value = [
            {"name": f"R{i}", "cuisine": "Italian",
             "brief_description": "Brief", "long_description": "Long"}
            for i in range(1, 4)
        ]
        mock_gemini.generate_airport_transport.side_effect = Exception("Gemini timeout")

        result = self.service.get_destination_content("FCO", "en")
        assert len(result.airport_transport.options) == 1
        assert result.airport_transport.options[0].mode == "taxi"

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_weather_fallback_on_gemini_failure(self, mock_loader, mock_gemini):
        """When weather fails, fallback 3-day forecast is used"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_weather.side_effect = Exception("Gemini timeout")

        result = self.service.get_weather("FCO", "en")
        assert len(result) == 3
        assert result[0].condition == "Sunny"

    @patch("app.services.destination_service.gemini_adapter")
    @patch("app.services.destination_service.csv_loader")
    def test_news_returns_empty_on_gemini_failure(self, mock_loader, mock_gemini):
        """When news fails, empty list is returned"""
        mock_loader.get_destination_info.return_value = {
            "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
            "emergency_contacts": EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            )
        }
        mock_gemini.generate_news.side_effect = Exception("Gemini timeout")

        result = self.service.get_news("FCO", "en")
        assert result == []


# ============================================================
# DESTINATION SERVICE — TRANSPORT MODE NORMALIZATION
# ============================================================

class TestTransportModeNormalization:
    """Test that creative Gemini mode names are normalized"""

    def test_train_variants(self):
        assert DestinationService._normalize_transport_mode("train") == "train"
        assert DestinationService._normalize_transport_mode("Tren (Elizabeth Line)") == "train"
        assert DestinationService._normalize_transport_mode("Metro") == "train"
        assert DestinationService._normalize_transport_mode("Leonardo Express (rail)") == "train"

    def test_bus_variants(self):
        assert DestinationService._normalize_transport_mode("bus") == "bus"
        assert DestinationService._normalize_transport_mode("Autobús urbano") == "bus"
        assert DestinationService._normalize_transport_mode("Airport Shuttle") == "bus"
        assert DestinationService._normalize_transport_mode("Coach service") == "bus"

    def test_taxi_default(self):
        assert DestinationService._normalize_transport_mode("taxi") == "taxi"
        assert DestinationService._normalize_transport_mode("Uber") == "taxi"
        assert DestinationService._normalize_transport_mode("Private Transfer") == "taxi"
        assert DestinationService._normalize_transport_mode("unknown") == "taxi"


# ============================================================
# DESTINATION SERVICE — FALLBACK STATIC METHODS
# ============================================================

class TestDestinationServiceStaticFallbacks:
    """Test static fallback methods directly"""

    def test_fallback_highlights_returns_5(self):
        highlights = DestinationService._fallback_highlights("Rome")
        assert len(highlights) == 5
        assert all(isinstance(h, Highlight) for h in highlights)
        assert highlights[0].id == "H001"

    def test_fallback_restaurants_returns_3(self):
        restaurants = DestinationService._fallback_restaurants("Rome")
        assert len(restaurants) == 3
        assert all(isinstance(r, Restaurant) for r in restaurants)
        cuisines = [r.cuisine for r in restaurants]
        assert "Local" in cuisines

    def test_fallback_weather_returns_3_days(self):
        forecasts = DestinationService._fallback_weather()
        assert len(forecasts) == 3
        assert all(isinstance(f, WeatherForecast) for f in forecasts)
        # Dates should be consecutive
        from datetime import datetime
        d0 = datetime.strptime(forecasts[0].date, "%Y-%m-%d")
        d1 = datetime.strptime(forecasts[1].date, "%Y-%m-%d")
        assert (d1 - d0).days == 1

    def test_fallback_transport_returns_taxi(self):
        transport = DestinationService._fallback_transport()
        assert len(transport.options) == 1
        assert transport.options[0].mode == "taxi"


# ============================================================
# INFLIGHT SERVICE — BIG FLOW ORCHESTRATION
# ============================================================

_DEST_INFO = {
    "destination": Destination(city="Rome", country="Italy", airport_code="FCO"),
    "emergency_contacts": EmergencyContacts(
        police="112", ambulance="118", fire="115",
        radio_taxi="+39", airport_info="+39", vueling_contact="+34"
    )
}


class TestInflightService:
    """Test the BIG FLOW orchestration"""

    def setup_method(self):
        self.service = InflightService()

    @patch("app.services.inflight_service.destination_service")
    @patch("app.services.inflight_service.flight_service")
    @patch("app.services.inflight_service.passenger_service")
    def test_orchestrates_all_five_services(self, mock_passenger, mock_flight, mock_dest):
        """BIG FLOW should call booking → flight → content → weather → news"""
        booking = _make_booking()
        mock_passenger.get_booking.return_value = booking
        mock_flight.get_flight.return_value = _make_flight()
        mock_dest.get_destination_content.return_value = DestinationContent(
            destination=Destination(city="Rome", country="Italy", airport_code="FCO"),
            highlights=[
                Highlight(id=f"H00{i}", title=f"Place {i}",
                         brief_description="Brief", long_description="Long")
                for i in range(1, 6)
            ],
            emergency_contacts=EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39", airport_info="+39", vueling_contact="+34"
            ),
            restaurants=[
                Restaurant(name=f"R{i}", cuisine="Italian",
                          brief_description="Brief", long_description="Long")
                for i in range(1, 4)
            ],
            airport_transport=AirportTransport(
                destination="main_train_station",
                options=[TransportOption(mode="train", estimated_duration_minutes=30, notes="Fast")]
            )
        )
        mock_dest.get_weather.return_value = [
            WeatherForecast(date="2026-02-09", condition="Sunny",
                          min_temperature_c=10.0, max_temperature_c=20.0)
        ]
        mock_dest.get_news.return_value = [
            LocalNews(title="Festival", brief_description="Brief",
                     long_description="Long", category="culture")
        ]

        result = self.service.get_inflight_experience("VY4K7M", "es")

        assert result.booking.booking_number == "VY4K7M"
        assert result.flight.flight_number == "VY71299"
        assert result.destination_content.destination.city == "Rome"
        assert len(result.weather) == 1
        assert len(result.news) == 1

        # Verify orchestration: booking date passed to flight
        mock_flight.get_flight.assert_called_once_with("VY71299", "20260207")
        # Verify destination fetched for booking's airport
        mock_dest.get_destination_content.assert_called_once_with("FCO", "es")

    @patch("app.services.inflight_service.passenger_service")
    def test_booking_not_found_raises(self, mock_passenger):
        """BIG FLOW fails fast when booking doesn't exist"""
        mock_passenger.get_booking.side_effect = ValueError("Booking not found: XXXXX")

        with pytest.raises(ValueError, match="Booking not found"):
            self.service.get_inflight_experience("XXXXX", "en")

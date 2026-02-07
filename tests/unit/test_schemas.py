"""Unit tests for Pydantic schema validation and cardinality constraints"""

import pytest
from pydantic import ValidationError
from app.models.schemas import (
    Passenger, Booking, Flight, Aircraft, CockpitCrew, CrewMember,
    CabinCrewMember, Destination, Highlight, Restaurant, EmergencyContacts,
    TransportOption, AirportTransport, WeatherForecast, LocalNews,
    DestinationContent, InflightExperience, ErrorResponse, ErrorDetail
)


# ============================================================
# FIXTURES — Reusable valid data builders
# ============================================================

def make_crew_member(first="Sofia", last="Conti"):
    """Cockpit crew member (captain / first officer) — full name"""
    return CrewMember(first_name=first, last_name=last)


def make_cabin_crew(first="Sofia"):
    """Cabin crew member — first name only (privacy)"""
    return CabinCrewMember(first_name=first)


def make_highlight(id_num=1):
    return Highlight(
        id=f"H00{id_num}",
        title=f"Place {id_num}",
        brief_description="A short description",
        long_description="A longer description with more detail"
    )


def make_restaurant(name="Da Enzo"):
    return Restaurant(
        name=name,
        cuisine="Italian",
        brief_description="Great pasta",
        long_description="Detailed review of the restaurant"
    )


def make_transport_option(mode="train"):
    return TransportOption(
        mode=mode,
        estimated_duration_minutes=30,
        notes="Every 15 minutes"
    )


def make_weather(date="2026-02-07"):
    return WeatherForecast(
        date=date,
        condition="Sunny",
        min_temperature_c=12.0,
        max_temperature_c=22.0
    )


def make_news(title="Good News", category="sports"):
    return LocalNews(
        title=title,
        brief_description="Brief summary",
        long_description="Full story details",
        category=category
    )


# ============================================================
# PASSENGER SCHEMA
# ============================================================

class TestPassengerSchema:

    def test_valid_passenger(self):
        p = Passenger(
            user_id="P001",
            first_name="Angel",
            last_name="Lopez",
            preferred_language="es"
        )
        assert p.user_id == "P001"

    def test_passenger_default_language_is_english(self):
        p = Passenger(user_id="P001", first_name="A", last_name="B")
        assert p.preferred_language == "en"

    def test_passenger_frequent_flyer_optional(self):
        p = Passenger(user_id="P001", first_name="A", last_name="B")
        assert p.frequent_flyer_number is None


# ============================================================
# FLIGHT SCHEMA — Cardinality: exactly 3 cabin crew
# ============================================================

class TestFlightSchema:

    def _make_flight(self, cabin_crew_count=3):
        return Flight(
            flight_number="VY71299",
            flight_date="20260207",
            departure_time="14:30",
            arrival_time="16:15",
            origin="BCN",
            destination="FCO",
            aircraft=Aircraft(
                model="Airbus A320",
                registration="EC-MXY",
                age_years=9,
                aircraft_name="Spirit of Barcelona"
            ),
            cockpit_crew=CockpitCrew(
                captain=make_crew_member("Laura", "Rossi"),
                first_officer=make_crew_member("Marco", "Bianchi")
            ),
            cabin_crew=[make_cabin_crew() for _ in range(cabin_crew_count)],
            average_duration_minutes=105,
            departure_gate="B23",
            baggage_claim_belt="Carousel 5"
        )

    def test_valid_flight_with_three_cabin_crew(self):
        flight = self._make_flight(3)
        assert len(flight.cabin_crew) == 3

    def test_flight_rejects_two_cabin_crew(self):
        with pytest.raises(ValidationError):
            self._make_flight(2)

    def test_flight_rejects_four_cabin_crew(self):
        with pytest.raises(ValidationError):
            self._make_flight(4)

    def test_flight_rejects_zero_cabin_crew(self):
        with pytest.raises(ValidationError):
            self._make_flight(0)


# ============================================================
# DESTINATION CONTENT — Cardinality: 5 highlights, 3 restaurants
# ============================================================

class TestDestinationContentSchema:

    def _make_content(self, highlights_count=5, restaurants_count=3, transport_count=2):
        return DestinationContent(
            destination=Destination(city="Rome", country="Italy", airport_code="FCO"),
            highlights=[make_highlight(i) for i in range(1, highlights_count + 1)],
            emergency_contacts=EmergencyContacts(
                police="112", ambulance="118", fire="115",
                radio_taxi="+39 06 3570", airport_info="+39 06 65951",
                vueling_contact="+34 931 518 158"
            ),
            restaurants=[make_restaurant(f"Restaurant {i}") for i in range(restaurants_count)],
            airport_transport=AirportTransport(
                destination="main_train_station",
                options=[make_transport_option() for _ in range(transport_count)]
            )
        )

    def test_valid_content_5_highlights_3_restaurants(self):
        content = self._make_content(5, 3)
        assert len(content.highlights) == 5
        assert len(content.restaurants) == 3

    def test_rejects_4_highlights(self):
        with pytest.raises(ValidationError):
            self._make_content(highlights_count=4)

    def test_rejects_6_highlights(self):
        with pytest.raises(ValidationError):
            self._make_content(highlights_count=6)

    def test_rejects_2_restaurants(self):
        with pytest.raises(ValidationError):
            self._make_content(restaurants_count=2)

    def test_rejects_4_restaurants(self):
        with pytest.raises(ValidationError):
            self._make_content(restaurants_count=4)

    def test_transport_allows_1_to_3_options(self):
        for count in [1, 2, 3]:
            content = self._make_content(transport_count=count)
            assert len(content.airport_transport.options) == count

    def test_transport_rejects_zero_options(self):
        with pytest.raises(ValidationError):
            self._make_content(transport_count=0)

    def test_transport_rejects_four_options(self):
        with pytest.raises(ValidationError):
            self._make_content(transport_count=4)


# ============================================================
# TRANSPORT OPTION — mode must be train/bus/taxi
# ============================================================

class TestTransportOptionSchema:

    def test_valid_modes(self):
        for mode in ["train", "bus", "taxi"]:
            option = make_transport_option(mode)
            assert option.mode == mode

    def test_rejects_invalid_mode(self):
        with pytest.raises(ValidationError):
            TransportOption(
                mode="helicopter",
                estimated_duration_minutes=15,
                notes="Fast"
            )


# ============================================================
# LOCAL NEWS — category must be valid
# ============================================================

class TestLocalNewsSchema:

    def test_valid_categories(self):
        for category in ["sports", "culture", "events", "local_interest"]:
            news = make_news(category=category)
            assert news.category == category

    def test_rejects_invalid_category(self):
        with pytest.raises(ValidationError):
            LocalNews(
                title="Bad",
                brief_description="Bad",
                long_description="Bad",
                category="crime"
            )


# ============================================================
# ERROR RESPONSE
# ============================================================

class TestErrorResponseSchema:

    def test_valid_error_response(self):
        error = ErrorResponse(
            code="PASSENGER_FLIGHT_MISMATCH",
            message="Flight numbers do not match",
            step="validate_consistency"
        )
        assert error.code == "PASSENGER_FLIGHT_MISMATCH"

    def test_error_with_details(self):
        error = ErrorResponse(
            code="SCHEMA_VALIDATION_FAILED",
            message="Missing field",
            step="validate_schema",
            details=ErrorDetail(field="highlights", reason="Expected 5, got 4")
        )
        assert error.details.field == "highlights"

    def test_error_details_optional(self):
        error = ErrorResponse(
            code="WEATHER_UNAVAILABLE",
            message="API down",
            step="get_weather"
        )
        assert error.details is None

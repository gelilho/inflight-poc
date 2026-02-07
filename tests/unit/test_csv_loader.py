"""Unit tests for CSV data loader"""

import pytest
from data.loaders.csv_loader import CSVDataLoader


@pytest.fixture
def loader():
    """Fresh CSV loader instance"""
    return CSVDataLoader()


class TestGetPassenger:
    """Tests for passenger lookup"""

    def test_existing_passenger_returns_correct_data(self, loader):
        passenger = loader.get_passenger("P001")
        assert passenger is not None
        assert passenger.user_id == "P001"
        assert passenger.first_name == "Angel"
        assert passenger.last_name == "Lopez"
        assert passenger.preferred_language == "es"

    def test_existing_passenger_has_frequent_flyer(self, loader):
        passenger = loader.get_passenger("P001")
        assert passenger.frequent_flyer_number == "VY123456789"

    def test_nonexistent_passenger_returns_none(self, loader):
        passenger = loader.get_passenger("P999")
        assert passenger is None

    def test_all_three_passengers_loadable(self, loader):
        for user_id in ["P001", "P002", "P003"]:
            passenger = loader.get_passenger(user_id)
            assert passenger is not None
            assert passenger.user_id == user_id


class TestGetBooking:
    """Tests for booking lookup"""

    def test_existing_booking_returns_correct_data(self, loader):
        booking = loader.get_booking("VY4K7M")
        assert booking is not None
        assert booking.booking_number == "VY4K7M"
        assert booking.user_id == "P001"
        assert booking.flight_number == "VY71299"
        assert booking.seat == "14D"
        assert booking.origin == "BCN"
        assert booking.destination == "FCO"

    def test_booking_date_is_string(self, loader):
        booking = loader.get_booking("VY4K7M")
        assert isinstance(booking.flight_date, str)
        assert booking.flight_date == "20260207"

    def test_booking_has_airport_names(self, loader):
        booking = loader.get_booking("VY4K7M")
        assert booking.origin_airport_name == "Barcelona El Prat"
        assert booking.destination_airport_name == "Rome Fiumicino"

    def test_nonexistent_booking_returns_none(self, loader):
        booking = loader.get_booking("XXXXXX")
        assert booking is None

    def test_all_three_bookings_loadable(self, loader):
        for pnr in ["VY4K7M", "VY8L2P", "VY3M9R"]:
            booking = loader.get_booking(pnr)
            assert booking is not None


class TestGetBookingsByUser:
    """Tests for user bookings lookup"""

    def test_user_with_one_booking(self, loader):
        bookings = loader.get_bookings_by_user("P003")
        assert len(bookings) == 1
        assert bookings[0].booking_number == "VY3M9R"

    def test_user_with_no_bookings_returns_empty(self, loader):
        bookings = loader.get_bookings_by_user("P999")
        assert bookings == []


class TestGetFlight:
    """Tests for flight lookup"""

    def test_existing_flight_returns_correct_data(self, loader):
        flight = loader.get_flight("VY71299", "20260207")
        assert flight is not None
        assert flight.flight_number == "VY71299"
        assert flight.origin == "BCN"
        assert flight.destination == "FCO"

    def test_flight_has_aircraft_details(self, loader):
        flight = loader.get_flight("VY71299", "20260207")
        assert flight.aircraft.model == "Airbus A320-200"
        assert flight.aircraft.registration == "EC-MXY"
        assert flight.aircraft.age_years == 9

    def test_flight_has_cockpit_crew(self, loader):
        flight = loader.get_flight("VY71299", "20260207")
        assert flight.cockpit_crew.captain.first_name == "Laura"
        assert flight.cockpit_crew.captain.last_name == "Rossi"
        assert flight.cockpit_crew.first_officer.first_name == "Marco"

    def test_flight_has_three_cabin_crew(self, loader):
        flight = loader.get_flight("VY71299", "20260207")
        assert len(flight.cabin_crew) == 3
        assert flight.cabin_crew[0].first_name == "Sofia"

    def test_flight_has_operational_details(self, loader):
        flight = loader.get_flight("VY71299", "20260207")
        assert flight.average_duration_minutes == 105
        assert flight.departure_gate == "B23"
        assert flight.baggage_claim_belt == "Carousel 5"

    def test_same_flight_different_dates_returns_different_aircraft(self, loader):
        flight_day1 = loader.get_flight("VY71299", "20260207")
        flight_day2 = loader.get_flight("VY71299", "20260208")
        assert flight_day1.aircraft.registration != flight_day2.aircraft.registration

    def test_nonexistent_flight_returns_none(self, loader):
        flight = loader.get_flight("XX9999", "20260207")
        assert flight is None

    def test_wrong_date_returns_none(self, loader):
        flight = loader.get_flight("VY71299", "20991231")
        assert flight is None


class TestGetDestinationInfo:
    """Tests for destination lookup"""

    def test_existing_destination_returns_data(self, loader):
        dest = loader.get_destination_info("FCO")
        assert dest is not None
        assert dest["destination"].city == "Rome"
        assert dest["destination"].country == "Italy"
        assert dest["destination"].airport_code == "FCO"

    def test_destination_has_emergency_contacts(self, loader):
        dest = loader.get_destination_info("FCO")
        contacts = dest["emergency_contacts"]
        assert contacts.police == "112"
        assert contacts.ambulance == "118"
        assert contacts.fire == "115"

    def test_nonexistent_destination_returns_none(self, loader):
        dest = loader.get_destination_info("XXX")
        assert dest is None

    def test_all_three_destinations_loadable(self, loader):
        for code in ["FCO", "LHR", "CDG"]:
            dest = loader.get_destination_info(code)
            assert dest is not None

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal


# ============ PASSENGER ============

class Passenger(BaseModel):
    user_id: str
    first_name: str
    last_name: str
    frequent_flyer_number: Optional[str] = None
    preferred_language: str = "en"


# ============ BOOKING ============

class Booking(BaseModel):
    booking_number: str           # PNR: "VY4K7M"
    user_id: str
    flight_number: str
    flight_date: str              # "20260207" (YYYYMMDD)
    seat: str
    origin: str                   # "BCN"
    origin_airport_name: str      # "Barcelona El Prat"
    destination: str              # "FCO"
    destination_airport_name: str # "Rome Fiumicino"
    baggage_claim_belt: str
    booking_class: str            # "Economy" / "Business"
    status: str                   # "confirmed" / "checked_in"


# ============ FLIGHT (Date-Specific) ============

class Aircraft(BaseModel):
    model: str
    registration: str             # Plate (EC-MXY)
    age_years: int
    aircraft_name: str            # "Spirit of Barcelona"


class CrewMember(BaseModel):
    """Cockpit crew member (captain / first officer) — full name public"""
    first_name: str
    last_name: str


class CabinCrewMember(BaseModel):
    """Cabin crew member — first name only (privacy)"""
    first_name: str


class CockpitCrew(BaseModel):
    captain: CrewMember
    first_officer: CrewMember


class Flight(BaseModel):
    flight_number: str
    flight_date: str              # "20260207" (YYYYMMDD)
    departure_time: str           # "14:30"
    arrival_time: str             # "16:15"
    origin: str
    destination: str
    aircraft: Aircraft
    cockpit_crew: CockpitCrew
    cabin_crew: List[CabinCrewMember] = Field(..., min_length=3, max_length=3)
    average_duration_minutes: int
    departure_gate: str
    baggage_claim_belt: str


# ============ DESTINATION CONTENT ============

class Destination(BaseModel):
    city: str
    country: str
    airport_code: str


class Highlight(BaseModel):
    id: str
    title: str
    brief_description: str        # 1 sentence
    long_description: str         # 2-3 paragraphs


class EmergencyContacts(BaseModel):
    police: str
    ambulance: str
    fire: str
    radio_taxi: str
    airport_info: str
    vueling_contact: str


class Restaurant(BaseModel):
    name: str
    cuisine: str
    brief_description: str        # 1 sentence
    long_description: str         # 2-3 paragraphs


class TransportOption(BaseModel):
    mode: Literal["train", "bus", "taxi"]
    estimated_duration_minutes: int
    notes: str


class AirportTransport(BaseModel):
    destination: str = "main_train_station"
    options: List[TransportOption] = Field(..., min_length=1, max_length=3)


class WeatherForecast(BaseModel):
    date: str  # YYYY-MM-DD
    condition: str
    min_temperature_c: float
    max_temperature_c: float


class LocalNews(BaseModel):
    title: str
    brief_description: str        # 1 sentence
    long_description: str         # 2-3 paragraphs
    category: Literal["sports", "culture", "events", "local_interest"]


class DestinationContent(BaseModel):
    destination: Destination
    highlights: List[Highlight] = Field(..., min_length=5, max_length=5)
    emergency_contacts: EmergencyContacts
    restaurants: List[Restaurant] = Field(..., min_length=3, max_length=3)
    airport_transport: AirportTransport


# ============ COMPOSED RESPONSES ============

class InflightExperience(BaseModel):
    """Complete inflight experience"""
    booking: Booking
    flight: Flight
    destination_content: DestinationContent
    weather: List[WeatherForecast]
    news: List[LocalNews]


# ============ ERROR SCHEMA ============

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    reason: str


class ErrorResponse(BaseModel):
    code: str
    message: str
    step: str
    details: Optional[ErrorDetail] = None

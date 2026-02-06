import pandas as pd
from pathlib import Path
from typing import Optional, List
from app.models.schemas import (
    Passenger, Booking, Flight, Aircraft, CockpitCrew, 
    CrewMember, EmergencyContacts, Destination
)


class CSVDataLoader:
    """Load mock data from CSV files"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent / "mock"
    
    def get_passenger(self, user_id: str) -> Optional[Passenger]:
        """Load passenger data"""
        df = pd.read_csv(self.data_dir / "passengers.csv")
        row = df[df["user_id"] == user_id]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        return Passenger(
            user_id=row["user_id"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            frequent_flyer_number=row.get("frequent_flyer_number"),
            preferred_language=row["preferred_language"]
        )
    
    def get_booking(self, booking_number: str) -> Optional[Booking]:
        """Load booking data by booking number (PNR)"""
        df = pd.read_csv(self.data_dir / "bookings.csv")
        row = df[df["booking_number"] == booking_number]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        return Booking(
            booking_number=row["booking_number"],
            user_id=row["user_id"],
            flight_number=row["flight_number"],
            flight_date=row["flight_date"],
            seat=row["seat"],
            origin=row["origin"],
            origin_airport_name=row["origin_airport_name"],
            destination=row["destination"],
            destination_airport_name=row["destination_airport_name"],
            baggage_claim_belt=row["baggage_claim_belt"],
            booking_class=row["booking_class"],
            status=row["status"]
        )
    
    def get_bookings_by_user(self, user_id: str) -> List[Booking]:
        """Get all bookings for a user"""
        df = pd.read_csv(self.data_dir / "bookings.csv")
        rows = df[df["user_id"] == user_id]
        
        bookings = []
        for _, row in rows.iterrows():
            bookings.append(Booking(
                booking_number=row["booking_number"],
                user_id=row["user_id"],
                flight_number=row["flight_number"],
                flight_date=row["flight_date"],
                seat=row["seat"],
                origin=row["origin"],
                origin_airport_name=row["origin_airport_name"],
                destination=row["destination"],
                destination_airport_name=row["destination_airport_name"],
                baggage_claim_belt=row["baggage_claim_belt"],
                booking_class=row["booking_class"],
                status=row["status"]
            ))
        
        return bookings
    
    def get_flight(self, flight_number: str, flight_date: str) -> Optional[Flight]:
        """Load flight data for specific date"""
        df = pd.read_csv(self.data_dir / "flights.csv")
        row = df[(df["flight_number"] == flight_number) & (df["flight_date"] == flight_date)]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        return Flight(
            flight_number=row["flight_number"],
            flight_date=row["flight_date"],
            departure_time=row["departure_time"],
            arrival_time=row["arrival_time"],
            origin=row["origin"],
            destination=row["destination"],
            aircraft=Aircraft(
                model=row["aircraft_model"],
                registration=row["registration"],
                age_years=int(row["age_years"]),
                aircraft_name=row["aircraft_name"]
            ),
            cockpit_crew=CockpitCrew(
                captain=CrewMember(
                    first_name=row["captain_first"],
                    last_name=row["captain_last"]
                ),
                first_officer=CrewMember(
                    first_name=row["fo_first"],
                    last_name=row["fo_last"]
                )
            ),
            cabin_crew=[
                CrewMember(first_name=row["crew1_first"], last_name=row["crew1_last"]),
                CrewMember(first_name=row["crew2_first"], last_name=row["crew2_last"]),
                CrewMember(first_name=row["crew3_first"], last_name=row["crew3_last"]),
            ],
            average_duration_minutes=int(row["avg_duration_min"]),
            departure_gate=row["departure_gate"],
            baggage_claim_belt=row["baggage_belt"]
        )
    
    def get_destination_info(self, airport_code: str) -> Optional[dict]:
        """Load destination basic info"""
        df = pd.read_csv(self.data_dir / "destinations.csv", dtype=str)
        row = df[df["airport_code"] == airport_code]
        
        if row.empty:
            return None
        
        row = row.iloc[0]
        return {
            "destination": Destination(
                city=row["city"],
                country=row["country"],
                airport_code=row["airport_code"]
            ),
            "emergency_contacts": EmergencyContacts(
                police=str(row["police"]),
                ambulance=str(row["ambulance"]),
                fire=str(row["fire"]),
                radio_taxi=str(row["radio_taxi"]),
                airport_info=str(row["airport_info"]),
                vueling_contact=str(row["vueling_contact"])
            )
        }


# Singleton instance
csv_loader = CSVDataLoader()

"""FLOW B: Passenger & Flight Context Service"""

from app.models.schemas import PassengerContext, ErrorResponse, ErrorDetail
from data.loaders.csv_loader import csv_loader
import logging

logger = logging.getLogger(__name__)


class FlowBService:
    """Service for retrieving passenger and flight context"""
    
    def get_passenger_context(self, user_id: str) -> PassengerContext:
        """
        FLOW B: Retrieve passenger and flight context
        
        Steps:
        1. Get passenger details
        2. Get flight operational details
        3. Validate consistency
        """
        
        logger.info(f"Starting FLOW B for user: {user_id}")
        
        # Step 1: Get passenger
        passenger = csv_loader.get_passenger(user_id)
        if not passenger:
            raise ValueError(f"Passenger not found: {user_id}")
        
        logger.info(f"Passenger loaded: {passenger.first_name} {passenger.last_name}")
        
        # Step 2: Get flight
        flight = csv_loader.get_flight(passenger.flight_number)
        if not flight:
            raise ValueError(f"Flight not found: {passenger.flight_number}")
        
        logger.info(f"Flight loaded: {flight.flight_number}")
        
        # Step 3: Validate consistency
        if passenger.flight_number != flight.flight_number:
            raise ValueError(
                f"Passenger flight mismatch: {passenger.flight_number} != {flight.flight_number}"
            )
        
        logger.info("FLOW B validation passed")
        
        return PassengerContext(
            passenger=passenger,
            flight=flight
        )


# Singleton instance
flow_b_service = FlowBService()

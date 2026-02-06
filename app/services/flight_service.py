"""Flight Service - Handle flight operations"""

from app.models.schemas import Flight
from data.loaders.csv_loader import csv_loader
import logging

logger = logging.getLogger(__name__)


class FlightService:
    """Service for flight operations"""
    
    def get_flight(self, flight_number: str, flight_date: str) -> Flight:
        """
        Get flight details for specific date
        
        Args:
            flight_number: Flight number (e.g., "VY71299")
            flight_date: Date in YYYY-MM-DD format (e.g., "2026-02-07")
        """
        logger.info(f"Fetching flight: {flight_number} on {flight_date}")
        
        flight = csv_loader.get_flight(flight_number, flight_date)
        if not flight:
            raise ValueError(
                f"Flight not found: {flight_number} on {flight_date}. "
                "Check flight number and date are correct."
            )
        
        return flight


# Singleton instance
flight_service = FlightService()

"""Passenger Service - Handle passenger and booking operations"""

from app.models.schemas import Passenger, Booking
from data.loaders.csv_loader import csv_loader
from typing import List
import logging

logger = logging.getLogger(__name__)


class PassengerService:
    """Service for passenger operations"""
    
    def get_passenger(self, user_id: str) -> Passenger:
        """Get passenger by user_id"""
        logger.info(f"Fetching passenger: {user_id}")
        
        passenger = csv_loader.get_passenger(user_id)
        if not passenger:
            raise ValueError(f"Passenger not found: {user_id}")
        
        return passenger
    
    def get_booking(self, booking_number: str) -> Booking:
        """Get booking by booking number (PNR)"""
        logger.info(f"Fetching booking: {booking_number}")
        
        booking = csv_loader.get_booking(booking_number)
        if not booking:
            raise ValueError(f"Booking not found: {booking_number}")
        
        return booking
    
    def get_passenger_bookings(self, user_id: str) -> List[Booking]:
        """Get all bookings for a passenger"""
        logger.info(f"Fetching bookings for passenger: {user_id}")
        
        # Verify passenger exists
        passenger = csv_loader.get_passenger(user_id)
        if not passenger:
            raise ValueError(f"Passenger not found: {user_id}")
        
        bookings = csv_loader.get_bookings_by_user(user_id)
        return bookings


# Singleton instance
passenger_service = PassengerService()

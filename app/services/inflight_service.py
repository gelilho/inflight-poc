"""Inflight Experience Service - Orchestrate complete experience"""

from app.models.schemas import InflightExperience
from app.services.passenger_service import passenger_service
from app.services.flight_service import flight_service
from app.services.destination_service import destination_service
import logging

logger = logging.getLogger(__name__)


class InflightService:
    """Service for orchestrating complete inflight experience"""
    
    def get_inflight_experience(self, booking_number: str, language: str) -> InflightExperience:
        """
        Get complete inflight experience based on booking
        
        Orchestrates:
        1. Booking details
        2. Flight details (for booking's date)
        3. Destination content (translated)
        4. Weather forecast
        5. Local news
        """
        logger.info(f"Generating inflight experience for booking: {booking_number} in {language}")
        
        # Get booking
        booking = passenger_service.get_booking(booking_number)
        
        # Get flight details for the booking's specific date
        flight = flight_service.get_flight(booking.flight_number, booking.flight_date)
        
        # Get destination content
        destination_content = destination_service.get_destination_content(
            booking.destination,
            language
        )
        
        # Get weather
        weather = destination_service.get_weather(booking.destination, language)
        
        # Get news
        news = destination_service.get_news(booking.destination, language)
        
        # Compose complete experience
        experience = InflightExperience(
            booking=booking,
            flight=flight,
            destination_content=destination_content,
            weather=weather,
            news=news
        )
        
        logger.info("Inflight experience generated successfully")
        return experience


# Singleton instance
inflight_service = InflightService()

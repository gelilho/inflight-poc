"""BIG FLOW: Combined Inflight Experience Service"""

from app.models.schemas import InflightExperience
from app.services.flow_a_service import flow_a_service
from app.services.flow_b_service import flow_b_service
from data.loaders.csv_loader import csv_loader
import logging

logger = logging.getLogger(__name__)


class BigFlowService:
    """Service for orchestrating complete inflight experience"""
    
    def generate_inflight_experience(self, user_id: str) -> InflightExperience:
        """
        BIG FLOW: Combine FLOW A + FLOW B
        
        Steps:
        1. Execute FLOW B (get passenger context)
        2. Extract destination from passenger data
        3. Execute FLOW A (generate destination experience)
        4. Aggregate results
        """
        
        logger.info(f"Starting BIG FLOW for user: {user_id}")
        
        # Execute FLOW B
        logger.info("Executing FLOW B...")
        passenger_context = flow_b_service.get_passenger_context(user_id)
        
        # Determine destination airport code
        destination = passenger_context.passenger.destination
        
        # Map destination to airport code (simple mapping for POC)
        # In production, this would be a proper lookup
        airport_code_map = {
            "Rome FCO": "FCO",
            "FCO": "FCO",
            "London": "LHR",
            "LHR": "LHR",
            "Paris": "CDG",
            "CDG": "CDG"
        }
        
        airport_code = airport_code_map.get(destination, "FCO")
        logger.info(f"Destination airport resolved: {airport_code}")
        
        # Execute FLOW A
        logger.info("Executing FLOW A...")
        destination_experience = flow_a_service.execute_flow_a(airport_code)
        
        # Combine results
        inflight_experience = InflightExperience(
            passenger_context=passenger_context,
            destination_experience=destination_experience
        )
        
        logger.info("BIG FLOW completed successfully")
        return inflight_experience


# Singleton instance
big_flow_service = BigFlowService()

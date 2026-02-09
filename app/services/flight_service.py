"""Flight Service - Handle flight operations"""

from typing import List
from app.models.schemas import Flight, FlightAdvisory
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
            flight_date: Date in YYYYMMDD format (e.g., "20260207")
        """
        logger.info(f"Fetching flight: {flight_number} on {flight_date}")

        flight = csv_loader.get_flight(flight_number, flight_date)
        if not flight:
            raise ValueError(
                f"Flight not found: {flight_number} on {flight_date}. "
                "Check flight number and date are correct."
            )

        return flight

    @staticmethod
    def get_flight_advisories() -> List[FlightAdvisory]:
        """Return standard flight advisories for passengers.

        These are regulatory / safety messages shown on the home screen.
        """
        return [
            FlightAdvisory(
                icon="📱",
                title="Modo Avión activado",
                description="Mantén tu dispositivo en Modo Avión durante todo el vuelo. Puedes usar la WiFi de a bordo una vez activado.",
                priority="high",
            ),
            FlightAdvisory(
                icon="📶",
                title="Datos móviles desactivados",
                description="Desactiva los datos móviles y el roaming. Usa únicamente la red WiFi del avión para navegar.",
                priority="high",
            ),
            FlightAdvisory(
                icon="🔋",
                title="Bluetooth permitido",
                description="Puedes usar auriculares Bluetooth y dispositivos de bajo consumo durante el vuelo.",
                priority="low",
            ),
            FlightAdvisory(
                icon="💺",
                title="Cinturón de seguridad",
                description="Mantén el cinturón abrochado mientras estés sentado, incluso con la señal apagada.",
                priority="medium",
            ),
        ]


# Singleton instance
flight_service = FlightService()

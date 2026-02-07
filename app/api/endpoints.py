"""FastAPI endpoints - Resource-oriented API design"""

from fastapi import APIRouter, HTTPException, Path
from app.models.schemas import (
    Passenger, Booking, Flight, DestinationContent,
    WeatherForecast, LocalNews, InflightExperience
)
from app.services.passenger_service import passenger_service
from app.services.flight_service import flight_service
from app.services.destination_service import destination_service
from app.services.inflight_service import inflight_service
from config.constants import SUPPORTED_LANGUAGES
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# ============================================================
# HEALTH & INFO
# ============================================================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "inflight-experience-poc",
        "supported_languages": SUPPORTED_LANGUAGES
    }


@router.get("/")
async def root():
    """API information and available endpoints"""
    return {
        "service": "Inflight Experience API - MWC PoC",
        "version": "2.0.0",
        "documentation": "/docs",
        "supported_languages": SUPPORTED_LANGUAGES,
        "data_sources": {
            "ai_content": "Google Gemini 2.5 Flash",
            "weather": "OpenWeatherMap API (fallback: mock data)",
            "news": "NewsAPI.org (fallback: Gemini-generated)"
        },
        "endpoints": {
            "passenger": "/api/v1/passenger/{user_id}",
            "passenger_bookings": "/api/v1/passenger/{user_id}/bookings",
            "booking": "/api/v1/booking/{booking_number}",
            "flight": "/api/v1/flight/{flight_number}/{date}",
            "destination_content": "/api/v1/destination/{airport_code}/content/{language}",
            "weather": "/api/v1/destination/{airport_code}/weather/{language}",
            "news": "/api/v1/destination/{airport_code}/news/{language}",
            "inflight_experience": "/api/v1/inflight-experience/{booking_number}/{language}"
        },
        "examples": {
            "passenger": "/api/v1/passenger/P001",
            "booking": "/api/v1/booking/VY4K7M",
            "flight": "/api/v1/flight/VY71299/20260207",
            "destination_rome_spanish": "/api/v1/destination/FCO/content/es",
            "weather_rome": "/api/v1/destination/FCO/weather/en",
            "news_rome": "/api/v1/destination/FCO/news/it",
            "full_experience": "/api/v1/inflight-experience/VY4K7M/es"
        }
    }


# ============================================================
# PASSENGER ENDPOINTS
# ============================================================

@router.get(
    "/api/v1/passenger/{user_id}",
    response_model=Passenger,
    summary="Get passenger information"
)
async def get_passenger(
    user_id: str = Path(..., description="Passenger user ID", examples=["P001"])
):
    """
    Get passenger personal information.
    
    Returns: name, frequent flyer number, preferred language
    """
    try:
        return passenger_service.get_passenger(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching passenger: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get(
    "/api/v1/passenger/{user_id}/bookings",
    response_model=List[Booking],
    summary="Get all bookings for a passenger"
)
async def get_passenger_bookings(
    user_id: str = Path(..., description="Passenger user ID", examples=["P001"])
):
    """
    Get all bookings associated with a passenger.
    
    Returns: list of bookings with flight details, seats, dates
    """
    try:
        return passenger_service.get_passenger_bookings(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching bookings: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ============================================================
# BOOKING ENDPOINT
# ============================================================

@router.get(
    "/api/v1/booking/{booking_number}",
    response_model=Booking,
    summary="Get booking details by booking number"
)
async def get_booking(
    booking_number: str = Path(..., description="Booking number (PNR)", examples=["VY4K7M"])
):
    """
    Get booking details by booking number (PNR).
    
    Returns: flight number, date, seat, origin, destination, baggage claim
    
    **This is what passengers scan from their boarding pass.**
    """
    try:
        return passenger_service.get_booking(booking_number)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching booking: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ============================================================
# FLIGHT ENDPOINT
# ============================================================

@router.get(
    "/api/v1/flight/{flight_number}/{date}",
    response_model=Flight,
    summary="Get flight operational details for specific date"
)
async def get_flight(
    flight_number: str = Path(..., description="Flight number", examples=["VY71299"]),
    date: str = Path(..., description="Flight date (YYYYMMDD)", examples=["20260207"])
):
    """
    Get flight operational details for a specific date.
    
    **Date format: YYYYMMDD (e.g., 20260207)**
    
    **Date-specific because crew, aircraft, and gates change daily.**
    
    Returns:
    - Aircraft details (model, registration, name, age)
    - Cockpit crew (captain, first officer)
    - Cabin crew (3 members)
    - Gates, times, duration
    """
    try:
        return flight_service.get_flight(flight_number, date)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching flight: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


# ============================================================
# DESTINATION ENDPOINTS
# ============================================================

@router.get(
    "/api/v1/destination/{airport_code}/content/{language}",
    response_model=DestinationContent,
    summary="Get destination content (AI-generated)"
)
async def get_destination_content(
    airport_code: str = Path(..., description="Airport code", examples=["FCO"]),
    language: str = Path(..., description="Language code", examples=["es"])
):
    """
    Get complete destination content including:
    - Basic info (city, country, airport)
    - Emergency contacts (police, ambulance, fire, taxi, airport, Vueling)
    - Top 5 highlights (with brief + long descriptions)
    - Top 3 restaurants (with brief + long descriptions)
    - Airport transport options
    
    **Data Source:** Google Gemini 2.5 Flash (AI-generated)
    
    **Translation:** All content translated to specified language
    
    **Note:** First call may take 10-20 seconds as AI generates content.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported: {SUPPORTED_LANGUAGES}"
        )
    
    try:
        logger.info(f"Starting destination content generation for {airport_code} in {language}")
        return destination_service.get_destination_content(airport_code, language)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching destination content: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get(
    "/api/v1/destination/{airport_code}/weather/{language}",
    response_model=List[WeatherForecast],
    summary="Get 3-day weather forecast"
)
async def get_weather(
    airport_code: str = Path(..., description="Airport code", examples=["FCO"]),
    language: str = Path(..., description="Language code", examples=["en"])
):
    """
    Get 3-day weather forecast for destination.
    
    **Data Source:** 
    - Primary: OpenWeatherMap API (real weather data)
    - Fallback: Mock data (if API unavailable or key invalid)
    
    **Translation:** Weather conditions translated to specified language
    
    Returns: 3-day forecast with min/max temperatures (°C) and conditions
    """
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported: {SUPPORTED_LANGUAGES}"
        )
    
    try:
        return destination_service.get_weather(airport_code, language)
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch weather")


@router.get(
    "/api/v1/destination/{airport_code}/news/{language}",
    response_model=List[LocalNews],
    summary="Get local news headlines"
)
async def get_news(
    airport_code: str = Path(..., description="Airport code", examples=["FCO"]),
    language: str = Path(..., description="Language code", examples=["it"])
):
    """
    Get 5 local news headlines for destination.
    
    **Data Source:**
    - Primary: NewsAPI.org (real news articles from last 7 days)
    - Filtering: Python code filters out dramatic/violent content for inflight safety
    - Fallback: Google Gemini generates safe, relevant news (if API unavailable)
    
    **Translation:** All news content translated to specified language
    
    **Content Safety:** 
    - Excludes: violence, crime, disasters, terrorism
    - Includes: sports, culture, events, local interest
    
    Returns: 5 news items with title, brief + long descriptions, and category
    
    **Note:** First call may take 10-15 seconds if using Gemini fallback.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported: {SUPPORTED_LANGUAGES}"
        )
    
    try:
        return destination_service.get_news(airport_code, language)
    except Exception as e:
        logger.error(f"Error fetching news: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch news: {str(e)}")


# ============================================================
# INFLIGHT EXPERIENCE (BIG FLOW)
# ============================================================

@router.get(
    "/api/v1/inflight-experience/{booking_number}/{language}",
    response_model=InflightExperience,
    summary="Complete inflight experience (BIG FLOW)"
)
async def get_inflight_experience(
    booking_number: str = Path(..., description="Booking number (PNR)", examples=["VY4K7M"]),
    language: str = Path(..., description="Language code", examples=["es"])
):
    """
    **THE BIG FLOW** - Complete inflight experience in one call.
    
    Combines:
    - Booking details (seat, baggage, airports)
    - Flight details (aircraft, crew, gates)
    - Destination content (highlights, restaurants, emergency contacts) - AI-generated
    - Weather forecast (OpenWeatherMap or mock)
    - Local news (NewsAPI or Gemini fallback)
    
    **Data Sources:**
    - AI Content: Google Gemini 2.5 Flash
    - Weather: OpenWeatherMap API (fallback: mock)
    - News: NewsAPI.org (fallback: Gemini)
    
    **Translation:** All content in specified language
    
    **Perfect for the full passenger experience.**
    
    **Note:** First call may take 30-45 seconds as content is generated.
    """
    if language not in SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {language}. Supported: {SUPPORTED_LANGUAGES}"
        )
    
    try:
        logger.info(f"Starting BIG FLOW for {booking_number} in {language}")
        return inflight_service.get_inflight_experience(booking_number, language)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating inflight experience: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

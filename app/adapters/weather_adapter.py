"""Weather Adapter - OpenWeatherMap API Integration"""

import requests
from typing import List, Dict
from datetime import datetime, timedelta
from config.settings import get_settings
from config.constants import AIRPORT_COORDINATES
import logging

logger = logging.getLogger(__name__)


class WeatherAdapter:
    """Weather adapter using OpenWeatherMap API"""

    def __init__(self):
        self.settings = get_settings()
        self.base_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.airport_coords = AIRPORT_COORDINATES
    
    def get_forecast(self, airport_code: str, days: int = 3) -> List[Dict]:
        """Get weather forecast from OpenWeatherMap"""
        
        # Check if we have API key
        if not self.settings.weather_api_key or self.settings.use_mock_data:
            logger.warning("Using mock weather data (no API key or mock mode enabled)")
            return self._get_mock_forecast(days)
        
        # Get coordinates
        coords = self.airport_coords.get(airport_code)
        if not coords:
            logger.warning(f"No coordinates for {airport_code}, using mock data")
            return self._get_mock_forecast(days)
        
        try:
            # Call OpenWeatherMap API
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": self.settings.weather_api_key,
                "units": "metric",  # Celsius
                "cnt": days * 8     # 8 forecasts per day (3-hour intervals)
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Process forecast data (group by day)
            return self._process_api_forecast(data, days)
        
        except Exception as e:
            logger.error(f"Weather API error: {e}, falling back to mock data")
            return self._get_mock_forecast(days)
    
    def _process_api_forecast(self, data: dict, days: int) -> List[Dict]:
        """Process OpenWeatherMap API response into our format"""
        
        forecasts = []
        daily_data = {}
        
        # Group forecasts by date
        for item in data.get("list", []):
            date_str = datetime.fromtimestamp(item["dt"]).strftime("%Y-%m-%d")
            
            if date_str not in daily_data:
                daily_data[date_str] = {
                    "temps": [],
                    "conditions": []
                }
            
            daily_data[date_str]["temps"].append(item["main"]["temp"])
            daily_data[date_str]["conditions"].append(
                item["weather"][0]["main"] if item.get("weather") else "Clear"
            )
        
        # Create daily summaries
        for date_str in sorted(daily_data.keys())[:days]:
            day_data = daily_data[date_str]
            
            forecasts.append({
                "date": date_str,
                "condition": max(set(day_data["conditions"]), key=day_data["conditions"].count),
                "min_temperature_c": round(min(day_data["temps"]), 1),
                "max_temperature_c": round(max(day_data["temps"]), 1)
            })
        
        return forecasts
    
    def _get_mock_forecast(self, days: int) -> List[Dict]:
        """Generate mock weather forecast"""
        base_date = datetime.now()
        
        forecasts = []
        conditions = ["Sunny", "Partly Cloudy", "Cloudy", "Clear"]
        
        for i in range(days):
            date = base_date + timedelta(days=i)
            forecasts.append({
                "date": date.strftime("%Y-%m-%d"),
                "condition": conditions[i % len(conditions)],
                "min_temperature_c": 12.0 + i,
                "max_temperature_c": 22.0 + i
            })
        
        return forecasts


# Singleton instance
weather_adapter = WeatherAdapter()

from typing import List, Dict
from datetime import datetime, timedelta


class WeatherAdapter:
    """Mock weather adapter (can be replaced with real API later)"""
    
    def get_forecast(self, airport_code: str, days: int = 3) -> List[Dict]:
        """Generate mock 3-day weather forecast"""
        
        # Mock data (in real implementation, call OpenWeatherMap API)
        base_date = datetime.now()
        
        forecasts = []
        for i in range(days):
            date = base_date + timedelta(days=i)
            forecasts.append({
                "date": date.strftime("%Y-%m-%d"),
                "condition": "Partly Cloudy" if i % 2 == 0 else "Sunny",
                "min_temperature_c": 12 + i,
                "max_temperature_c": 22 + i
            })
        
        return forecasts


# Singleton instance
weather_adapter = WeatherAdapter()

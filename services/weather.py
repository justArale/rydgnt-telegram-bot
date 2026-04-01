import logging
import httpx
from bot.config import Config
from core.models import WeatherData, Coordinates

logger = logging.getLogger(__name__)

# Open Meteo is free, open-source, no key needed. Also provides a 16-day forecast, which could be useful for planning rides for a specific day.
OPEN_METEO_URL = Config.OPEN_METEO_URL

# WMO Weather interpretation codes (WW) - https://open-meteo.com/en/docs#weathervariables (end of page)
WMO_CODES: dict[int, str] = {
0: "Clear sky",
1: "Mainly clear",
2: "Partly cloudy",
3: "Overcast",
45: "Fog",
48: "Depositng rime fog",
51: "Drizzle: Light intensity",
53: "Drizzle: Moderate intensity",
55: "Drizzle: Dense intensity",
56: "Freezing Drizzle: Light intensity",
57: "Freezing Drizzle: Dense intensity",
61: "Rain: Slight intensity",
63: "Rain: Moderate intensity",
65: "Rain: Heavy intensity",
66: "Freezing Rain: Light intensity",
67: "Freezing Rain: Heavy intensity",
71: "Snow fall: Slight intensity",
73: "Snow fall: Moderate intensity",
75: "Snow fall: Heavy intensity",
77: "Snow grains",
80: "Rain showers: Slight intensity",
81: "Rain showers: Moderate intensity",
82: "Rain showers: Violent intensity",
85: "Snow showers: Slight intensity",
86: "Snow showers: Heavy intensity",
95: "Thunderstorm: Slight or moderate intensity",
96: "Thunderstorm with slight hail",
99: "Thunderstorm with heavy hail"
}

# Conditions I don't want to ride -> should display an advice against riding
unsuitable_conditions = {56, 57, 65, 66, 67, 71, 73, 75, 77, 82, 86, 95, 96, 99} 

def _degrees_to_cardinal(degrees: float) -> str:
    """Convert wind direction in degrees to cardinal direction (N, NE, E, SE, S, SW, W, NW)"""
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(degrees / 22.5) % 16
    return directions[idx]

def _assess_suitability(conditions_code: int, wind_speed: float) -> tuple[bool, str]:
    """Determine if the weather conditions are suitable for cycling based on WMO code and wind speed.
    Returns a tuple of (is_suitable, reason_string).
    """
    if conditions_code in unsuitable_conditions:
        reason = f"'{WMO_CODES.get(conditions_code, 'Severe weather')}' forecast - not recommended for cycling."
        return False, reason
    if wind_speed > 40:
        reason = f"Very strong winds with {wind_speed} kph - might be not suitable for safe cycling."
        return False, reason
    if wind_speed > 30:
        reason = f"Strong winds with {wind_speed} kph - consider wind direction carefully."
        return False, reason
    
    return True, ""

async def get_weather_data(coords: Coordinates) -> WeatherData:
    """Fetch current weather condition for a coordinate."""
    params = {
        "longitude": coords.longitude,
        "latitude": coords.latitude,
        "current": [
            "temperature_2m",
            "apparent_temperature",
            "windspeed_10m",
            "winddirection_10m",
            "weather_code"
        ],
        "wind_speed_unit": "kmh",
        "timezone": "auto",
        "forecast_days": 1
    }

    logger.info("Fetching weather for %s", coords)

    async with httpx.AsyncClient() as client:
        response = await client.get(OPEN_METEO_URL, params=params)
        response.raise_for_status()
        
    data = response.json()

    # Open meteo nests the current weather data under "current"
    current = data.get("current", {})

    temp = current.get("temperature_2m", 0.0)
    feels_like = current.get("apparent_temperature", 0.0)
    wind_speed = current.get("windspeed_10m", 0.0)
    wind_dir_deg = current.get("winddirection_10m", 0.0)
    weather_code = current.get("weather_code", 0)

    wind_label = _degrees_to_cardinal(wind_dir_deg)
    condition_str = WMO_CODES.get(weather_code, f"Code {weather_code}")
    is_suitable, reason = _assess_suitability(weather_code, wind_speed)

    logger.info("Weather at %s: %s, %s°C (feels like %s°C), wind %s kph from %s - Suitable for cycling: %s. Reason: %s", coords, condition_str, temp, feels_like, wind_speed, wind_label, is_suitable, reason)

    return WeatherData(
        temperature_c=temp,
        feels_like_c=feels_like,
        wind_speed_kph=wind_speed,
        wind_direction_deg=wind_dir_deg,
        wind_direction_label=wind_label,
        condition=condition_str,
        is_good_for_cycling=is_suitable,
        is_good_reason=reason
    )
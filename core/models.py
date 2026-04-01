from dataclasses import dataclass, field
from typing import Optional

@dataclass
class WeatherData:
    """Current weather at a specific location."""
    temperature_c: float  = 0.0 # Celsius
    feels_like_c: float = 0.0 # Celsius
    wind_speed_kph: float = 0.0   # kph
    wind_direction_deg: float = 0.0  # degrees, 0=N. 90=E, 180=S, 270=W
    wind_direction_label: str = "N" # Human readable: N, NE, E, SE, S, SW, W, NW
    condition: str = "Unknown" # e.g. "Clear", "Cloudy", "Rain", etc.
    is_good_for_cycling: bool = True
    is_good_reason: str = "" # Explanation why if it's bad for cycling

    @property
    def tailwind_direction_deg(self) -> float:
        """Direction you should ride to have tailwind. If the wind comes from north, ride south"""
        return (self.wind_direction_deg + 180) % 360
    
import asyncio
from core.models import Coordinates
from services.weather import get_weather_data

async def main():
    # Test fetching with coordinates of berlin
    coords = Coordinates(
        latitude=52.5200,
        longitude=13.4050
    )

    weather = await get_weather_data(coords)

    print("\n--- Weather Data ---")
    print(weather)

if __name__ == "__main__":
    asyncio.run(main())
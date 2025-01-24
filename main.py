import requests
import json
import os
from datetime import datetime
from config import API_KEY, BASE_URL


def get_weather_data(city):
    try:
        # Update query parameters for WeatherAPI
        params = {"q": city, "key": API_KEY}  # Use 'key' instead of 'appid'
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city}: {e}")
        return None


def save_weather_data(city, data):
    if not os.path.exists("data"):
        os.makedirs("data")

    # Corrected filename
    filename = f"data/{city}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

    print(f"Data saved to {filename}")


def main():
    print("Weather data collector")
    cities = input("Enter city names separated by commas: ").split(",")

    for city in cities:
        city = city.strip()  # Remove any extra spaces around the city name
        print(f"\nFetching weather data for {city}...")

        data = get_weather_data(city)

        if data:
            # Parse WeatherAPI's response
            current = data["current"]
            print(f"Weather in {city}: {current['condition']['text']}, Temperature: {current['temp_c']}°C")
            save_weather_data(city, data)


if __name__ == "__main__":
    main()
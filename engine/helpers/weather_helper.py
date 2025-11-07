# engine/helpers/weather_helper.py

import requests
from engine.config import WEATHER_API_KEY # This will now work correctly

def get_weather(city):
    """
    Fetches weather data for a given city from OpenWeatherMap API.
    Returns a formatted string with the weather report or an error message.
    """
    if not WEATHER_API_KEY or WEATHER_API_KEY == "YOUR_API_KEY_HERE":
        return "Weather API key is missing. Please add it to engine/config.py."

    api_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    try:
        # Add a timeout to prevent the request from hanging indefinitely
        response = requests.get(api_url, timeout=5)
        # This will raise an HTTPError if the response was an HTTP error (e.g., 401, 404)
        response.raise_for_status() 
        
        data = response.json()

        # Extract data with .get() to avoid errors if a key is missing
        weather_desc = data.get("weather")[0].get("description")
        temp = round(data.get("main", {}).get("temp", 0))
        feels_like = round(data.get("main", {}).get("feels_like", 0))
        humidity = data.get("main", {}).get("humidity", 0)

        # Capitalize the city name for a nicer output
        city_name = data.get("name", city.capitalize())

        report = (
            f"The current weather in {city_name} is {weather_desc}. "
            f"The temperature is {temp} degrees Celsius, but it feels like {feels_like}. "
            f"The humidity is at {humidity} percent."
        )
        return report

    except requests.exceptions.HTTPError as http_err:
        # Handle specific HTTP errors, like 401 for an invalid API key
        if response.status_code == 401:
            return "Weather API key is invalid. Please check engine/config.py."
        elif response.status_code == 404:
            return f"Sorry, I couldn't find weather information for a city named '{city}'."
        else:
            print(f"HTTP error occurred: {http_err}")
            return "An error occurred while fetching weather data."
            
    except requests.exceptions.RequestException as req_err:
        # Handle network-related errors (e.g., no internet connection)
        print(f"Network error occurred: {req_err}")
        return "Sorry, I'm having trouble connecting to the weather service. Please check your internet connection."

    except Exception as e:
        # A catch-all for any other unexpected errors
        print(f"An unexpected error occurred in get_weather: {e}")
        return "Sorry, an unexpected error occurred while fetching the weather."
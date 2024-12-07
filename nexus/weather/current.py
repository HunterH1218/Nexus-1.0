import requests
import random

def get_current_weather(lat, lon):
    # Construct the Open-Meteo URL for retrieving current weather
    current_weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"

    try:
        response = requests.get(current_weather_url)
        response.raise_for_status()
        weather_data = response.json()

        return weather_data['current_weather']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return {"error": "Failed to retrieve current weather data."}

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def get_weather_description(code):
    weather_descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_descriptions.get(code, "Unknown weather code")

def main():
    lat, lon = 40.7128, -74.0060
    current_weather = get_current_weather(lat, lon)

    if "error" in current_weather:
        print(current_weather["error"])
    else:
        temperature_c = current_weather['temperature']
        temperature_f = celsius_to_fahrenheit(temperature_c)
        weather_code = current_weather['weathercode']
        windspeed = current_weather['windspeed']
        winddirection = current_weather['winddirection']
        weather_condition = get_weather_description(weather_code)
        reponses = [
            f"It is currently {temperature_f}°F with {weather_condition.lower()}.",
            f"Yes sir, it is {temperature_f}°F and {weather_condition.lower()}.",
            f"The temperature is {temperature_f}°F and the weather is {weather_condition.lower()}.",
            f"The weather is {weather_condition.lower()} and the temperature is {temperature_f}°F."
            
        ]

        return random.choice(reponses)

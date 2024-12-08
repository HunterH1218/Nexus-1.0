import requests

# Mapping weather code to description
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

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def mm_to_inches(mm):
    return mm * 0.0393701

def get_seven_day_forecast():
    latitude = 40.7128
    longitude = -74.0060
    endpoint = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=auto"

    response = requests.get(endpoint)

    if response.status_code == 200:
        forecast_data = response.json()
        daily_data = forecast_data.get('daily', {})
        temperatures_max = daily_data.get('temperature_2m_max', [])
        temperatures_min = daily_data.get('temperature_2m_min', [])
        precipitation = daily_data.get('precipitation_sum', [])
        weather_conditions = daily_data.get('weathercode', [])
        time = daily_data.get('time', [])

        forecast_list = []

        for day, max_temp, min_temp, precip, condition in zip(time, temperatures_max, temperatures_min, precipitation, weather_conditions):
            forecast_entry = {
                "date": day,
                "max_temperature": celsius_to_fahrenheit(max_temp),
                "min_temperature": celsius_to_fahrenheit(min_temp),
                "precipitation": mm_to_inches(precip),
                "weather_condition": weather_descriptions.get(condition, "Unknown condition")
            }
            forecast_list.append(forecast_entry)

        # Return formatted result
        formatted_result = "\n".join(
            f"Date: {entry['date']}\n"
            f"Max Temperature: {entry['max_temperature']:.2f}°F\n"
            f"Min Temperature: {entry['min_temperature']:.2f}°F\n"
            f"Precipitation: {entry['precipitation']:.2f} inches\n"
            f"Weather Condition: {entry['weather_condition']}\n"
            for entry in forecast_list
        )
        return formatted_result
    else:
        return f"Error: Failed to retrieve data. Status code: {response.status_code}"



import requests
from datetime import datetime
import pytz

def get_weather_forecast(lat=40.7128, lon=-74.0060):  # Default coordinates for New York
    url = f"https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["temperature_2m", "precipitation_probability", "weathercode"],
        "timezone": "America/New_York"
    }

    response = requests.get(url, params=params)
    return response.json()

def get_weather_description(code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        95: "Thunderstorm"
    }
    return weather_codes.get(code, "Unknown")

def get_daily_forecast():
    # Get the current hour in EST
    est = pytz.timezone('America/New_York')
    current_time = datetime.now(est)
    current_hour = current_time.hour

    # Get weather data
    weather_data = get_weather_forecast()

    # Get the hourly data
    hours = weather_data['hourly']['time']
    temps = weather_data['hourly']['temperature_2m']
    precip = weather_data['hourly']['precipitation_probability']
    weather_codes = weather_data['hourly']['weathercode']

    # Find today's index in the data
    today = current_time.strftime('%Y-%m-%d')

    forecast_data = []

    for i, time_str in enumerate(hours):
        hour = datetime.fromisoformat(time_str).hour
        date = time_str.split('T')[0]

        if date == today and hour >= current_hour:
            weather_desc = get_weather_description(weather_codes[i])
            period = "AM" if hour < 12 else "PM"
            display_hour = hour if hour <= 12 else hour - 12
            display_hour = 12 if display_hour == 0 else display_hour
            temp_f = (temps[i] * 9/5) + 32

            forecast_data.append({
                "hour": f"{display_hour:02d}:00 {period}",
                "temperature": f"{temp_f:.1f}°F",
                "precipitation": f"{precip[i]}%",
                "conditions": weather_desc
            })

    return forecast_data

def format_forecast(forecast_data):
    formatted = []
    for hour_data in forecast_data:
        formatted.append(
            f"\nHour: {hour_data['hour']}\n"
            f"Temperature: {hour_data['temperature']}\n"
            f"Precipitation Probability: {hour_data['precipitation']}\n"
            f"Conditions: {hour_data['conditions']}\n"
        )
    return "".join(formatted)

def daily_forecast():
    forecast_data = get_daily_forecast()
    formatted_forecast = format_forecast(forecast_data)
    return formatted_forecast
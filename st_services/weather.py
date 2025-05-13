import requests, os
from dotenv import load_dotenv
from langchain.tools import Tool
import streamlit as st

load_dotenv()
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]


def get_weather_by_coordinates(location: str) -> str:
    '''
    location is of form [longitude, latitude]
    '''
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
    
    location = location.split(",")
    longitude = location[0].strip()
    latitude = location[1].strip()
    
    url = f"https://weather.googleapis.com/v1/currentConditions:lookup?key={GOOGLE_API_KEY}&location.longitude={longitude}&location.latitude={latitude}"
    print(f"\n{url}\n")
    response = requests.get(url)

    if response.status_code != 200:
        print(response.json())
        return "Error fetching weather data."
    
    data = response.json()
    if not data:
        return "Error fetching weather data."
    
    city = data["timeZone"]["id"].split("/")[1].replace("_", " ")
    real_temp = data["temperature"]["degrees"]
    feel_temp = data["feelsLikeTemperature"]["degrees"]
    
    return f"The temperature in {city} is currently {real_temp}°C, and feels like {feel_temp}°C."


def get_weather_by_address(location: str) -> str:
    '''
    location is of form address (as a string)
    '''
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set in environment variables.")
    
    address = location.replace(" ", "%")
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={GOOGLE_API_KEY}"

    response = requests.get(url)

    if response.status_code != 200:
        print(response.json())
        return "Error fetching weather data."
    
    data = response.json()
    coordinates = data["results"][0]["geometry"]["location"]
    coor_input = f"{coordinates['lng']}, {coordinates['lat']}"
    stmt = get_weather_by_coordinates(coor_input)
    stmt = stmt.split()
    stmt[3] = location
    return " ".join(stmt)


weather_by_address_tool = Tool(
    name="Weather By Address",
    func=get_weather_by_address,
    description="Get the current weather for a city. Provide the city name as input.",
    return_direct=True,             # so that the result is returned directly to the user, instead of being checked by the agent
)

weather_by_coordinates_tool = Tool(
    name="Weather By Coordinates",
    func=get_weather_by_coordinates,
    description="Get the current weather for a location. Provide the coordinates as input in the form longitude, latitude.",
    return_direct=True,             # so that the result is returned directly to the user, instead of being checked by the agent
)
import requests
import os
import logging
from urllib.parse import quote
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transfer_to_plan():
    from triage_agent.agents import plan_agent
    return plan_agent

def transfer_to_google_maps():
    from triage_agent.agents import google_maps_agent
    return google_maps_agent

def transfer_to_weather():
    from triage_agent.agents import weather_agent
    return weather_agent

def transfer_back_to_triage():
    from triage_agent.agents import triage_agent
    return triage_agent

def get_google_maps_directions(origin, destination, waypoints=None):
    logger.info(f"get_google_maps_directions called with origin: {origin}, destination: {destination}, waypoints: {waypoints}")
    
    try:
        # URL encode the origin and destination
        encoded_origin = quote(origin)
        encoded_destination = quote(destination)
        
        logger.info(f"Encoded origin: {encoded_origin}")
        logger.info(f"Encoded destination: {encoded_destination}")
        
        # Create a Google Maps URL with the route
        maps_url = f"https://www.google.com/maps/dir/?api=1&origin={encoded_origin}&destination={encoded_destination}"
        
        # Add waypoints if provided
        if waypoints:
            encoded_waypoints = "|".join(quote(wp) for wp in waypoints)
            maps_url += f"&waypoints={encoded_waypoints}"
            logger.info(f"Encoded waypoints: {encoded_waypoints}")
        
        logger.info(f"Generated Google Maps URL: {maps_url}")
        
        waypoints_str = f" via {', '.join(waypoints)}" if waypoints else ""
        result = {
            "url": maps_url,
            "message": f"Here's a Google Maps link with the route from {origin} to {destination}{waypoints_str}: {maps_url}"
        }
        
        logger.info(f"Returning result: {result}")
        
        return result
    except Exception as e:
        logger.error(f"Error in get_google_maps_directions: {str(e)}")
        return {"error": f"An error occurred: {str(e)}"}

def get_weather(location, time="now"):
    """Get the current weather in a given location using OpenWeatherMap API."""
    logger.info(f"get_weather called with location: {location}, time: {time}")
    
    api_key = "3d8f139292cf72433268ec1b62594143"
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        weather_info = {
            "location": location,
            "temperature": str(data["main"]["temp"]),
            "description": data["weather"][0]["description"],
            "time": time
        }
        
        logger.info(f"Weather info retrieved: {weather_info}")
        return json.dumps(weather_info)
    except Exception as e:
        logger.error(f"Error in get_weather: {str(e)}")
        return json.dumps({"error": f"Unable to fetch weather data: {str(e)}"})

from swarm import Swarm, Agent
import os
import dotenv
from triage_agent.tools import (
    transfer_to_plan,
    transfer_to_google_maps,
    transfer_to_weather,
    get_google_maps_directions,
    get_weather,
    transfer_back_to_triage
)
from triage_agent.prompts import (
    TRIAGE_INSTRUCTIONS,
    PLAN_INSTRUCTIONS,
    GOOGLE_MAPS_INSTRUCTIONS,
    WEATHER_INSTRUCTIONS
)

dotenv.load_dotenv()

# Set your OpenAI API key here
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

client = Swarm()

triage_agent = Agent(
    name="Triage Agent",
    instructions=TRIAGE_INSTRUCTIONS,
    model="gpt-4o",
    tools=[transfer_to_plan, transfer_to_google_maps, transfer_to_weather]
)

plan_agent = Agent(
    name="Plan Agent",
    instructions=PLAN_INSTRUCTIONS,
    model="gpt-4o",
    tools=[]
)

google_maps_agent = Agent(
    name="Google Maps Agent",
    instructions=GOOGLE_MAPS_INSTRUCTIONS,
    model="gpt-4o",
    tools=[get_google_maps_directions]
)

weather_agent = Agent(
    name="Weather Agent",
    instructions=WEATHER_INSTRUCTIONS,
    model="gpt-4o",
    tools=[get_weather]
)

# Set up functions for each agent
triage_agent.functions = [transfer_to_plan, transfer_to_google_maps, transfer_to_weather]
plan_agent.functions = [transfer_back_to_triage]
google_maps_agent.functions = [transfer_back_to_triage]
weather_agent.functions = [get_weather, transfer_back_to_triage]

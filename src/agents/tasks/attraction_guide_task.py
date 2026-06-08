from crewai import Task
from ..agent.attraction_agent import atrraction_guide_agents
from pydantic import BaseModel

class AttractionOutput(BaseModel):
    attractions: list
    travel_info: dict

attraction_tasks = Task(
    agent=atrraction_guide_agents,
    name="Attraction Guide Task",
    description="""Provide information about 10 most popular attractions and travel destinations for this specified location {location}.
                Instructions:
                - Retrieve information about attractions and travel destinations for the specified location.
                - Retrieve travel information for the specified location.
                - Analyze the retrieved data to provide a clear and concise summary of the attractions and travel information, including any significant events or changes in conditions.
                -Provide also list of activities that can be done on each attraction and travel destination.
                 - Provide a detailed advice and recommendations for the user that who has to travel on that location
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - attractions: A list of dictionaries containing information about attractions in the specified location.
    - travel_info: A dictionary containing travel information for the specified location.
    """,
    output_pydantic=AttractionOutput
)
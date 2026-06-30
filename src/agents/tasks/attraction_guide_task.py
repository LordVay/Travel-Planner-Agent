from crewai import Task
from ..agent.attraction_agent import atrraction_guide_agents
from pydantic import BaseModel

class AttractionOutput(BaseModel):
    attractions: list
    travel_info: dict

attraction_tasks = Task(
    agent=atrraction_guide_agents,
    name="Attraction Guide Task",
    description="""Provide information about the 10 most popular attractions and travel destinations for a group of {group_size} travelers
                visiting {location} for {days} days, with interests in {interests}, preferred intensity level of {intensity},
                and interest in events such as {events}.
                Instructions:
                - Retrieve information about attractions and travel destinations for the specified location.
                - Filter and prioritize attractions that match the group's interests: {interests}.
                - Consider the intensity level preference of {intensity} when recommending activities (e.g., relaxed sightseeing vs adventure activities).
                - Include relevant events ({events}) happening in the area during the travel period.
                - Consider the group size of {group_size} when recommending attractions (group-friendly activities, capacity, etc.).
                - Retrieve travel information for the specified location.
                - Analyze the retrieved data to provide a clear and concise summary of the attractions and travel information, including any significant events or changes in conditions.
                - Provide a list of activities that can be done on each attraction and travel destination.
                - Provide detailed advice and recommendations for the user traveling to that location.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - attractions: A list of dictionaries containing information about attractions in the specified location, including activities, suitability for the group, and intensity level.
    - travel_info: A dictionary containing travel information for the specified location.
    """,
    output_pydantic=AttractionOutput
)

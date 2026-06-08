from crewai import Task
from ..agent.itenerary_agent import itenerary_agents
from pydantic import BaseModel
from .attraction_guide_task import attraction_tasks

class IteneraryOutput(BaseModel):
    itinerary: list

itenerary_tasks = Task(
    agent=itenerary_agents,
    name="Itenerary Organizer Task",
    description="""Provide an optimized travel itinerary for a specified number of days ({days}) based on user preferences, travel constraints, and available options.
                Instructions:
                - Analyze user preferences, travel constraints, and available options to create an optimized travel itinerary for the specified number of days.
                - Consider factors such as weather conditions, attraction availability, and user preferences when organizing the itinerary.
                - Provide a clear and concise summary of the optimized travel itinerary, including recommended attractions, activities, and travel information for each day.
                - Provide advice to users on how to stay safe and comfortable in different weather scenarios while optimizing their travel itineraries.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    List of dictionaries per day with the following fields:
    - day: An integer representing the day of the itinerary.
    - attractions: A list of dictionaries containing information about recommended attractions and activities for that day.
    - travel_info: A dictionary containing travel information for that day, such as transportation options and estimated travel times.
    """,
    output_pydantic=IteneraryOutput,
    context=[attraction_tasks]
)
from crewai import Task
from ..agent.itenerary_agent import itenerary_agents
from pydantic import BaseModel
from .attraction_guide_task import attraction_tasks

class IteneraryOutput(BaseModel):
    itinerary: list

itenerary_tasks = Task(
    agent=itenerary_agents,
    name="Itenerary Organizer Task",
    description="""Provide an optimized travel itinerary for a group of {group_size} travelers visiting {location} for {days} days,
                with a total budget of {total_budget}, preferred schedule style of {schedule_style}, intensity level of {intensity},
                and interests in {interests}.
                Instructions:
                - Analyze user preferences including schedule style ({schedule_style}), intensity ({intensity}), and interests ({interests})
                  to create an optimized travel itinerary for {days} days.
                - Consider the group size of {group_size} when planning activities and logistics.
                - Stay within the total budget of {total_budget} when planning the overall itinerary.
                - Consider factors such as weather conditions, attraction availability, and user preferences when organizing the itinerary.
                - Organize the daily schedule according to the preferred schedule style: {schedule_style} (e.g., packed/relaxed/balanced).
                - Provide a clear and concise summary of the optimized travel itinerary, including recommended attractions, activities, and travel information for each day.
                - Provide advice to users on how to stay safe and comfortable in different weather scenarios while optimizing their travel itineraries.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    List of dictionaries per day with the following fields:
    - day: An integer representing the day of the itinerary.
    - schedule_style: The schedule approach for that day.
    - attractions: A list of dictionaries containing information about recommended attractions and activities for that day, matched to the group's interests and intensity preference.
    - travel_info: A dictionary containing travel information for that day, such as transportation options and estimated travel times.
    - estimated_cost: Estimated cost for that day's activities for the group.
    """,
    output_pydantic=IteneraryOutput,
    context=[attraction_tasks]
)

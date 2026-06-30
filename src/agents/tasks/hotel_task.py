from crewai import Task
from ..agent.hotel_agent import hotel_agents
from pydantic import BaseModel

class HotelOutput(BaseModel):
    hotels: list
    advice: str

hotel_tasks = Task(
    agent=hotel_agents,
    name="Hotel Recommendation Task",
    description="""Provide hotel recommendations for a group of {group_size} travelers visiting {location} for {days} days,
                with a total budget range of {total_budget} and hotel preference of {hotel_preference}.
                Instructions:
                - Use the hotel_finder tool to retrieve available hotel options for the specified location that are currently in operation.
                - Analyze the retrieved data to provide a clear and concise summary of the available hotels, including their rates, popularity, and user ratings.
                - Consider the group size of {group_size} when recommending room configurations and estimate total accommodation cost for the stay.
                - Filter and rank hotels that match the hotel preference: {hotel_preference}.
                - Ensure the recommended hotels fit within the total budget range of {total_budget} for {days} days.
                - Provide detailed advice and recommendations for the user on which hotels to consider based on their preferences and the available options.
                - Provide a ranking of the hotels based on popularity, price and user ratings, and make an estimated budget calculation for specific hotels.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - hotels: A list of dictionaries containing information about the available hotels that are currently open, including their rates, popularity, address, user ratings, and estimated total cost for the group.
    - advice: A string providing advice and recommendations based on the available hotel options, group size, budget, and preferences.
    """,
    output_pydantic=HotelOutput
)

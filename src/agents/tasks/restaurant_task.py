from crewai import Task
from ..agent.restaurant_agent import restaurant_agents
from pydantic import BaseModel

class RestaurantOutput(BaseModel):
    restaurants: list
    advice: str

restaurant_tasks = Task(
    agent=restaurant_agents,
    name="Restaurant Recommendation Task",
    description="""Provide restaurant recommendations for a group of {group_size} travelers visiting {location} for {days} days,
                considering their cuisine preference of {restaurant_preference}, dietary restrictions of {dietary_restrictions},
                and a meal budget per day of {meal_budget_per_day}.
                Instructions:
                - Use the restaurant_finder tool to retrieve available restaurant options for the specified location.
                - Analyze the retrieved data to provide a clear and concise summary of the available restaurants, including their rates, popularity, and user ratings.
                - Filter restaurants that match the cuisine preference: {restaurant_preference} and accommodate dietary restrictions: {dietary_restrictions}.
                - Provide research about the menus of the restaurants, the type of food they serve, best sellers, and if they have any special offers or discounts.
                - Estimate meal costs for the group of {group_size} and ensure recommendations fit within the daily meal budget of {meal_budget_per_day}.
                - Provide detailed advice and recommendations for the user on which restaurants to consider based on their preferences and the available options.
                - Provide a ranking of the restaurants based on popularity, price and user ratings, and make an estimated budget calculation for specific restaurants.
                - Make sure that the restaurant is currently in operation and not closed.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - restaurants: A list of dictionaries containing information about the available restaurants, including their rates, popularity, address, user ratings, cuisine type, and estimated meal cost for the group.
    - advice: A string providing advice and recommendations based on the available restaurant options, cuisine preferences, dietary restrictions, and budget constraints.
    """,
    output_pydantic=RestaurantOutput
)

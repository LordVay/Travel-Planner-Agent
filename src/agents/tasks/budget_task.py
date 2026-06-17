from crewai import Task
from ..agent.budget_agent import budget_agents
from pydantic import BaseModel
from .attraction_guide_task import attraction_tasks
from .itenerary_task import itenerary_tasks
from .hotel_task import hotel_tasks
from .restaurant_task import restaurant_tasks

class BudgetOutput(BaseModel):
    budget: dict
    advice: str
    diagrams: dict

budget_tasks = Task(
    agent=budget_agents,
    name="Budget Planning Task",
    description="""Provide a detailed budget plan for a specified trip.
                Instructions:
                - Use the all the tools available to retrieve information about the costs of different aspects of the trip, such as transportation, accommodation, food, and activities.
                - Analyze the retrieved data to provide a clear and concise summary of the available budget options, including their costs, value, and user ratings.
                - Provide diagrams and visualizations to help users understand the budget breakdown and tracking.
                - Provide detailed advice and recommendations for the user on how to manage their budget effectively based on their preferences and the available options.
                -Provide also a ranking of the budget options based on cost-effectiveness, value, and user ratings, and make an estimated budget calculation for specific options.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - budget: A dictionary containing information about the available budget options, including their costs, value, and user ratings.
    - advice: A string providing advice and recommendations based on the available budget options.
    - diagrams: budget track and breakdown that will be used on visualization to help users understand the budget breakdown and tracking.
    """,
    output_pydantic=BudgetOutput,
    context=[attraction_tasks, itenerary_tasks, hotel_tasks, restaurant_tasks]
)
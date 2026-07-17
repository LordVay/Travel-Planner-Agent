from crewai import Task
from ..agent.budget_agent import budget_agents
from pydantic import BaseModel
from .attraction_guide_task import attraction_tasks
from .itenerary_task import itenerary_tasks
from .hotel_task import hotel_tasks
from .restaurant_task import restaurant_tasks


class BudgetOutput(BaseModel):
    total_budget: float
    days: int
    group_size: int
    category_breakdown: list
    daily_spending: list
    advice: str


budget_tasks = Task(
    agent=budget_agents,
    name="Budget Planning Task",
    description="""Analyze and allocate a travel budget for {group_size} travelers visiting {location} for {days} days
                with a total budget of {total_budget}.

                Instructions:
                - Parse the total budget amount and work with numerical values.
                - Allocate the total budget across these categories: Accommodation, Meals, Transportation, Activities, Miscellaneous.
                - Calculate daily spending estimates for each day of the trip (day 1 through day {days}).
                - Use context from the hotel, restaurant, attraction, and itinerary agents to make realistic cost estimates.
                - Ensure all category amounts sum to the total budget.
                - Provide percentage allocation for each category.
                - Provide per-day breakdown showing how much is spent each day across all categories.
                - Give practical budget management advice based on the destination and group size.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - total_budget: The total budget as a number (e.g. 2000.0). Use the midpoint if a range is given.
    - days: Number of trip days as an integer.
    - group_size: Number of travelers as an integer.
    - category_breakdown: A list of dictionaries, each with keys:
        - category: string (one of "Accommodation", "Meals", "Transportation", "Activities", "Miscellaneous")
        - amount: number (allocated dollar amount for this category)
        - percentage: number (percentage of total budget, e.g. 35.0 for 35%)
    - daily_spending: A list of dictionaries (one per day), each with keys:
        - day: integer (day number starting from 1)
        - accommodation: number (daily accommodation cost)
        - meals: number (daily meals cost)
        - transportation: number (daily transport cost)
        - activities: number (daily activities cost)
        - miscellaneous: number (daily misc cost)
        - total: number (total spending for that day)
    - advice: A string with budget management tips and recommendations.
    """,
    output_pydantic=BudgetOutput,
    context=[attraction_tasks, itenerary_tasks, hotel_tasks, restaurant_tasks],
)
from crewai import Task
from ..agent.travel_planner_agent import travel_planner_agents
from ..tasks.weather_task import weather_tasks
from ..tasks.attraction_guide_task import attraction_tasks
from ..tasks.itenerary_task import itenerary_tasks
from ..tasks.hotel_task import hotel_tasks
from ..tasks.restaurant_task import restaurant_tasks
from pydantic import BaseModel


class TravelPlanOutput(BaseModel):
    trip_summary: dict
    daily_plan: list
    accommodation: dict
    dining_plan: dict
    budget_breakdown: dict
    packing_tips: list
    safety_advice: str


travel_planner_tasks = Task(
    agent=travel_planner_agents,
    name="Travel Planner Compilation Task",
    description="""Compile all outputs from the weather, attraction, hotel, restaurant, and itinerary agents into a comprehensive
                travel plan for a group of {group_size} travelers visiting {location} for {days} days with a total budget of {total_budget}.

                Instructions:
                - Review and synthesize all context provided by the other agents (weather, attractions, hotels, restaurants, itinerary).
                - Create a trip summary including destination, dates, group size, total budget, and key highlights.
                - Organize a day-by-day plan that integrates:
                    * Morning, afternoon, and evening activities from the itinerary and attraction agents.
                    * Recommended restaurants for each meal (breakfast, lunch, dinner) from the restaurant agent, matching cuisine preference ({restaurant_preference}) and dietary restrictions ({dietary_restrictions}).
                    * Weather-appropriate clothing and activity suggestions from the weather agent.
                - Include accommodation details from the hotel agent, matching preference ({hotel_preference}) and budget.
                - Provide a complete budget breakdown showing estimated costs for accommodation, meals, activities, and transportation for the group of {group_size}.
                - Ensure total estimated cost fits within {total_budget}.
                - Add packing tips based on weather forecast and planned activities.
                - Include safety advice and travel tips specific to {location}.
                - Match the schedule style ({schedule_style}) and intensity ({intensity}) preferences throughout.
                """,

    expected_output="""
    A structured JSON object with the following fields:
    - trip_summary: A dictionary with keys: destination, days, group_size, total_budget, highlights (list of top experiences), and travel_style.
    - daily_plan: A list of dictionaries per day, each containing:
        - day: Day number
        - weather_summary: Expected weather for that day
        - morning: Dictionary with activity, location, estimated_cost
        - afternoon: Dictionary with activity, location, estimated_cost
        - evening: Dictionary with activity, location, estimated_cost
        - meals: Dictionary with breakfast, lunch, dinner (each has restaurant_name, cuisine, estimated_cost_per_person)
        - notes: Any special tips for that day
    - accommodation: A dictionary with hotel_name, address, rating, estimated_total_cost, check_in, check_out, and room_configuration.
    - dining_plan: A dictionary with total_meal_budget, daily_meal_budget, cuisine_preferences, dietary_notes, and top_restaurant_picks (list).
    - budget_breakdown: A dictionary with accommodation_cost, meal_cost, activity_cost, transportation_cost, miscellaneous, and total_estimated_cost.
    - packing_tips: A list of strings with recommended items to pack.
    - safety_advice: A string with safety and travel tips for the destination.
    """,
    output_pydantic=TravelPlanOutput,
    context=[weather_tasks, attraction_tasks, itenerary_tasks, hotel_tasks, restaurant_tasks],
)

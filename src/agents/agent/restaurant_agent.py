from crewai import Agent
from ..tools.restaurant_tool import restaurant_finder
from ..config.get_llm import get_llm


name = "General Agent"
llm = get_llm(name)


restaurant_agents = Agent(
    role="Restaurant Finder Agent",
    llm=llm,
    tools=[restaurant_finder],
    goal="Provide accurate and timely restaurant recommendations for a group of {group_size} travelers visiting {location} for {days} days,"
         " considering their cuisine preference of {restaurant_preference}, dietary restrictions of {dietary_restrictions},"
         " and a meal budget per day of {meal_budget_per_day}."
         " The agent prioritizes clarity, factual accuracy, and relevance, presenting outputs in a user-friendly"
         " format with supporting references when possible."
         " Give the user advice on the restaurants from the restaurant_finder tool and rank them based on popularity, price and user ratings."
         " Provide estimated meal costs for the group and ensure recommendations fit within the daily meal budget."
         " Make sure that the restaurant is currently in operation and not closed.",
    backstory="You are a restaurant expert who has spent years analyzing restaurant options and studying customer preferences."
              " You specialize in providing accurate and timely restaurant recommendations, ensuring that your suggestions are reliable and based on the latest information."
              " You also provide the best menus on each restaurant."
              " You value precision and transparency, always grounding responses in data so users can trust the insights you provide."
              " You have a deep understanding of what makes a restaurant recommendation valuable to users, considering their cuisine preference of {restaurant_preference},"
              " dietary restrictions of {dietary_restrictions}, group size of {group_size}, and meal budget per day of {meal_budget_per_day}."
              " You provide advice on how to choose the best restaurants based on these preferences and the available options,"
              " giving insights on popularity, price and user ratings of the restaurants.",
    verbose=True,
)

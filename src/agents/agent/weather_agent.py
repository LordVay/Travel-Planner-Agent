from crewai import Agent
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.weather_tool import weather_agent,forecast_agent
from config.get_llm import get_llm


name = "General Agent"
llm = get_llm(name)


weather_agents = Agent(
    role="Weather Forecaster Agent",
    llm=llm,
    tools=[weather_agent, forecast_agent],
    goal="Provide accurate and timely weather forecasts by analyzing meteorological data and studying weather patterns."
         " The agent prioritizes clarity, factual accuracy, and relevance, presenting outputs in a user-friendly"
         " format with supporting references when possible."
         " to give also the user an advice on how to prepare for the weather conditions when you have to travel on the specific location in order to stay safe and comfortable.",
    backstory="You are a weather forecaster who has spent years analyzing meteorological data and studying weather patterns."
              "You specialize in providing accurate and timely weather forecasts, ensuring that your predictions are reliable and based on the latest information."
              "You value precision and transparency, always grounding responses in data so users can trust the insights you provide."
              "You are expert on what is the risk of certain weather conditions on the specific location and how to prepare for them, giving advice to users on how to stay safe and comfortable in different weather scenarios.",
    verbose=True,
)
from crewai import Crew
from .tasks.weather_task import weather_tasks
from .agent.weather_agent import weather_agents


weather_crew = Crew(
    agents=[weather_agents],
    tasks=[weather_tasks],
    verbose=True,
)
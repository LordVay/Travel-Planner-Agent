from crewai import Crew
from .tasks.weather_task import weather_tasks
from .agent.weather_agent import weather_agents
from .tasks.attraction_guide_task import attraction_tasks
from .agent.attraction_agent import atrraction_guide_agents
from .tasks.itenerary_task import itenerary_tasks
from .agent.itenerary_agent import itenerary_agents



weather_crew = Crew(
    agents=[weather_agents],
    tasks=[weather_tasks],
    verbose=True,
)

attraction_crew = Crew(
    agents=[atrraction_guide_agents],
    tasks=[attraction_tasks],
    verbose=True,
    )

itenerary_crew = Crew(
    agents=[atrraction_guide_agents, itenerary_agents],
    tasks=[attraction_tasks, itenerary_tasks],
    verbose=True,
    )
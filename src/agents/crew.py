from crewai import Crew
from .tasks.weather_task import weather_tasks
from .agent.weather_agent import weather_agents
from .tasks.attraction_guide_task import attraction_tasks
from .agent.attraction_agent import atrraction_guide_agents
from .tasks.itenerary_task import itenerary_tasks
from .agent.itenerary_agent import itenerary_agents
from .tasks.hotel_task import hotel_tasks
from .agent.hotel_agent import hotel_agents
from .tasks.restaurant_task import restaurant_tasks
from .agent.restaurant_agent import restaurant_agents



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

hotel_crew = Crew(
    agents=[hotel_agents],
    tasks=[hotel_tasks],
    verbose=True,
)

restaurant_crew = Crew(
    agents=[restaurant_agents],
    tasks=[restaurant_tasks],
    verbose=True,
)
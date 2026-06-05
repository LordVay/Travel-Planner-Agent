from crewai import LLM
from .llm_config import LLM_CONFIG
from .api import AgentSettings
agent = AgentSettings()



def get_llm(agent_name):
    model = LLM_CONFIG.get(agent_name, {}).get("model")
    temperature = LLM_CONFIG.get(agent_name, {}).get("temperature")
    llm = LLM(
        model=model,
        temperature=temperature,
        api_key=agent.GEMINI_API
    )
    return llm
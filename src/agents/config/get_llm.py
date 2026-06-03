from crewai import LLM
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.llm_config import LLM_CONFIG
from config.api import AgentSettings
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
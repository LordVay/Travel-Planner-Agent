from crewai import LLM
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from config.llm_config import LLM_CONFIG


def get_llm(agent_name):
    model = LLM_CONFIG.get(agent_name, {}).get("model")
    temperature = LLM_CONFIG.get(agent_name, {}).get("temperature")
    llm = LLM(
        model=model,
        temperature=temperature,
    )
    return llm
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class AgentSettings(BaseSettings):
    WEATHER_API : str
    GEMINI_API : str
    FLIGHT_API : str
    MAPS_API : str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

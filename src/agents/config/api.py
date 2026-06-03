from pydantic_settings import BaseSettings

class AgentSettings(BaseSettings):
    WEATHER_API : str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"

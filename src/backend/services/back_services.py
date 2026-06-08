from ...agents.crew import weather_crew
from ...agents.crew import attraction_crew


def get_weather_forecast(location: str) -> dict:
    input_data = {
        "location": location
    }
    try:
        result = weather_crew.kickoff(input_data)
        result_dict = result.to_dict()
        return result_dict
    except ValueError as e:
        print(f"Invalid location: {str(e)}")
        raise
    
def get_attraction_guide(location: str) -> dict:
    input_data = {
        "location": location
    }  
    try:
        result = attraction_crew.kickoff(input_data)
        result_dict = result.to_dict()
        return result_dict
    except ValueError as e:
        print(f"Invalid location: {str(e)}")
        raise
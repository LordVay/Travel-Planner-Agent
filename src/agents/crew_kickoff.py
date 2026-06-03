from pprint import pprint
from crew import weather_crew

input_data = {
    "location": "New York City"
}

result = weather_crew.kickoff(input_data)

result_dict = result.to_dict()

pprint(result_dict)
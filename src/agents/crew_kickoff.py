from pprint import pprint

if __package__ in (None, ""):
    import os
    import sys

    # Allow running this file directly: python src/agents/crew_kickoff.py
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from src.agents.crew import restaurant_crew
else:
    from .crew import restaurant_crew


def main() -> None:
    input_data = {
        # General parameters
        "location": "Bolinao, Pangasinan, Philippines",
        "days": 3,
        "group_size": 4,
        "total_budget": "$1500 - $2000",
        # Restaurant and Hotel specific
        "restaurant_preference": "Filipino cuisine, seafood",
        "dietary_restrictions": "None",
        "meal_budget_per_day": "$50",
        "hotel_preference": "beachfront resort, mid-range",
        # Attraction and Itinerary specific
        "interests": "beaches, snorkeling, historical sites, nature",
        "intensity": "moderate",
        "events": "local festivals, cultural events",
        "schedule_style": "balanced",
    }

    result = restaurant_crew.kickoff(input_data)
    result_dict = result.to_dict()
    pprint(result_dict)


if __name__ == "__main__":
    main()

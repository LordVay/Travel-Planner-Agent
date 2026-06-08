from pprint import pprint

if __package__ in (None, ""):
    import os
    import sys

    # Allow running this file directly: python src/agents/crew_kickoff.py
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    from src.agents.crew import itenerary_crew
else:
    from .crew import itenerary_crew


def main() -> None:
    input_data = {
        "days": 5,
        "location": "Bolinao, Pangasinan, Philippines",
    }

    result = itenerary_crew.kickoff(input_data)
    result_dict = result.to_dict()
    pprint(result_dict)


if __name__ == "__main__":
    main()
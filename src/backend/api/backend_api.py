import logging
from fastapi import APIRouter, HTTPException
from ..services.back_services import get_weather_forecast
from ..services.back_services import get_attraction_guide

router = APIRouter()

@router.post("/travel/forecast")
def forecast(location: str):
    try:
        result = get_weather_forecast(location)
        return result
    except ValueError as e:
        # Return 400 Bad Request for invalid city
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Return 500 for unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.post("/travel/attractions")
def attractions(location: str):
    try:
        result = get_attraction_guide(location)
        return result
    except ValueError as e:
        # Return 400 Bad Request for invalid city
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Return 500 for unexpected errors
        raise HTTPException(status_code=500, detail="Internal server error")
# API route definitions for the TravelAgent backend.
# Security features applied per endpoint:
#   - @limiter.limit("10/minute"): Rate limits each IP to 10 requests/minute
#   - LocationRequest/ItineraryRequest: Validates and sanitizes input before processing
#   - Request parameter: Required by slowapi to identify the client IP for rate limiting
# Unhandled exceptions are caught by the global exception handlers in main.py.

from fastapi import APIRouter, HTTPException, Request
from ..models.requests import LocationRequest, ItineraryRequest
from ..middleware.rate_limit import limiter
from ..services.back_services import (
    get_weather_forecast,
    get_attraction_guide,
    get_itenerary,
    get_hotel_recommendation,
    get_restaurant_recommendation,
)

router = APIRouter()


@router.post("/travel/forecast")
@limiter.limit("10/minute")
def forecast(request: Request, body: LocationRequest):
    """Get weather forecast for a location. Input is sanitized via LocationRequest."""
    try:
        return get_weather_forecast(body.location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/attractions")
@limiter.limit("10/minute")
def attractions(request: Request, body: LocationRequest):
    """Get tourist attractions for a location. Input is sanitized via LocationRequest."""
    try:
        return get_attraction_guide(body.location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/hotels")
@limiter.limit("10/minute")
def hotels(request: Request, body: LocationRequest):
    """Get hotel recommendations for a location. Input is sanitized via LocationRequest."""
    try:
        return get_hotel_recommendation(body.location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/restaurants")
@limiter.limit("10/minute")
def restaurants(request: Request, body: LocationRequest):
    """Get restaurant recommendations for a location. Input is sanitized via LocationRequest."""
    try:
        return get_restaurant_recommendation(body.location)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/itenerary")
@limiter.limit("10/minute")
def itenerary(request: Request, body: ItineraryRequest):
    """Generate a multi-day itinerary. Input is sanitized via ItineraryRequest (location + days 1-30)."""
    try:
        return get_itenerary(body.location, body.days)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
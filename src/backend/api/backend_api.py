# API route definitions for the TravelAgent backend.
# Security features applied per endpoint:
#   - @limiter.limit("10/minute"): Rate limits each IP to 10 requests/minute
#   - Request models: Validates and sanitizes input before processing
#   - Request parameter: Required by slowapi to identify the client IP for rate limiting
# Unhandled exceptions are caught by the global exception handlers in main.py.

from fastapi import APIRouter, HTTPException, Request
from ..models.requests import (
    LocationRequest,
    HotelRequest,
    RestaurantRequest,
    AttractionRequest,
    ItineraryRequest,
    TravelPlanRequest,
)
from ..middleware.rate_limit import limiter
from ..services.back_services import (
    get_weather_forecast,
    get_attraction_guide,
    get_itenerary,
    get_hotel_recommendation,
    get_restaurant_recommendation,
    get_travel_plan,
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
def attractions(request: Request, body: AttractionRequest):
    """Get tourist attractions for a location. Input is sanitized via AttractionRequest."""
    try:
        return get_attraction_guide(
            body.location,
            body.days,
            body.group_size,
            body.interests,
            body.intensity,
            body.events,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/hotels")
@limiter.limit("10/minute")
def hotels(request: Request, body: HotelRequest):
    """Get hotel recommendations. Input is sanitized via HotelRequest."""
    try:
        return get_hotel_recommendation(
            body.location,
            body.days,
            body.group_size,
            body.total_budget,
            body.hotel_preference,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/restaurants")
@limiter.limit("10/minute")
def restaurants(request: Request, body: RestaurantRequest):
    """Get restaurant recommendations. Input is sanitized via RestaurantRequest."""
    try:
        return get_restaurant_recommendation(
            body.location,
            body.days,
            body.group_size,
            body.restaurant_preference,
            body.dietary_restrictions,
            body.meal_budget_per_day,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/itenerary")
@limiter.limit("10/minute")
def itenerary(request: Request, body: ItineraryRequest):
    """Generate a multi-day itinerary. Input is sanitized via ItineraryRequest."""
    try:
        return get_itenerary(
            body.location,
            body.days,
            body.group_size,
            body.total_budget,
            body.interests,
            body.intensity,
            body.events,
            body.schedule_style,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/travel/plan")
@limiter.limit("10/minute")
def travel_plan(request: Request, body: TravelPlanRequest):
    """Generate a full travel plan compiling all agents. Input is sanitized via TravelPlanRequest."""
    try:
        return get_travel_plan(
            body.location,
            body.days,
            body.group_size,
            body.total_budget,
            body.restaurant_preference,
            body.dietary_restrictions,
            body.meal_budget_per_day,
            body.hotel_preference,
            body.interests,
            body.intensity,
            body.events,
            body.schedule_style,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

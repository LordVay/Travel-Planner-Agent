# Input validation models for API request bodies.
# These enforce input sanitization at the API boundary — rejecting malicious payloads
# (XSS, SQL injection, command injection) before they reach business logic.

import re
from pydantic import BaseModel, Field, field_validator


def _sanitize_text_field(v: str) -> str:
    """Strip whitespace and reject characters outside the allowed set.
    Allows: letters, accented chars, digits, spaces, hyphens, apostrophes, periods, commas, parentheses, slashes.
    Blocks: <, >, ;, quotes, brackets, etc. — preventing injection attacks."""
    v = v.strip()
    if not re.match(r"^[a-zA-Z0-9\s\-\'.,()\/À-ɏ]+$", v):
        raise ValueError(
            "Field must contain only letters, digits, spaces, hyphens, "
            "apostrophes, periods, commas, and slashes"
        )
    return v


def _sanitize_location(v: str) -> str:
    """Strip whitespace and reject any characters outside the allowed set.
    Allows: letters, accented chars (À-ɏ), spaces, hyphens, apostrophes, periods, commas, parentheses.
    Blocks: <, >, ;, quotes, brackets, etc. — preventing injection attacks."""
    v = v.strip()
    if not re.match(r"^[a-zA-Z\s\-\'.,()À-ɏ]+$", v):
        raise ValueError(
            "Location must contain only letters, spaces, hyphens, "
            "apostrophes, periods, and commas"
        )
    return v


class LocationRequest(BaseModel):
    """Request body for endpoints that accept a location string."""

    location: str = Field(..., min_length=2, max_length=100)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        return _sanitize_location(v)


class HotelRequest(BaseModel):
    """Request body for the hotel recommendation endpoint."""

    location: str = Field(..., min_length=2, max_length=100)
    days: int = Field(..., ge=1, le=30)
    group_size: int = Field(..., ge=1, le=50)
    total_budget: str = Field(..., min_length=1, max_length=50)
    hotel_preference: str = Field(..., min_length=1, max_length=200)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        return _sanitize_location(v)

    @field_validator("total_budget", "hotel_preference")
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        return _sanitize_text_field(v)


class RestaurantRequest(BaseModel):
    """Request body for the restaurant recommendation endpoint."""

    location: str = Field(..., min_length=2, max_length=100)
    days: int = Field(..., ge=1, le=30)
    group_size: int = Field(..., ge=1, le=50)
    restaurant_preference: str = Field(..., min_length=1, max_length=200)
    dietary_restrictions: str = Field(..., min_length=1, max_length=200)
    meal_budget_per_day: str = Field(..., min_length=1, max_length=50)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        return _sanitize_location(v)

    @field_validator("restaurant_preference", "dietary_restrictions", "meal_budget_per_day")
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        return _sanitize_text_field(v)


class AttractionRequest(BaseModel):
    """Request body for the attraction guide endpoint."""

    location: str = Field(..., min_length=2, max_length=100)
    days: int = Field(..., ge=1, le=30)
    group_size: int = Field(..., ge=1, le=50)
    interests: str = Field(..., min_length=1, max_length=300)
    intensity: str = Field(..., min_length=1, max_length=50)
    events: str = Field(..., min_length=1, max_length=300)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        return _sanitize_location(v)

    @field_validator("interests", "intensity", "events")
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        return _sanitize_text_field(v)


class ItineraryRequest(BaseModel):
    """Request body for the itinerary endpoint — requires all travel parameters."""

    location: str = Field(..., min_length=2, max_length=100)
    days: int = Field(..., ge=1, le=30)
    group_size: int = Field(..., ge=1, le=50)
    total_budget: str = Field(..., min_length=1, max_length=50)
    interests: str = Field(..., min_length=1, max_length=300)
    intensity: str = Field(..., min_length=1, max_length=50)
    events: str = Field(..., min_length=1, max_length=300)
    schedule_style: str = Field(..., min_length=1, max_length=50)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        return _sanitize_location(v)

    @field_validator("total_budget", "interests", "intensity", "events", "schedule_style")
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        return _sanitize_text_field(v)


class TravelPlanRequest(BaseModel):
    """Request body for the full travel planner endpoint — compiles all agents into one plan."""

    location: str = Field(..., min_length=2, max_length=100)
    days: int = Field(..., ge=1, le=30)
    group_size: int = Field(..., ge=1, le=50)
    total_budget: str = Field(..., min_length=1, max_length=50)
    restaurant_preference: str = Field(..., min_length=1, max_length=200)
    dietary_restrictions: str = Field(..., min_length=1, max_length=200)
    meal_budget_per_day: str = Field(..., min_length=1, max_length=50)
    hotel_preference: str = Field(..., min_length=1, max_length=200)
    interests: str = Field(..., min_length=1, max_length=300)
    intensity: str = Field(..., min_length=1, max_length=50)
    events: str = Field(..., min_length=1, max_length=300)
    schedule_style: str = Field(..., min_length=1, max_length=50)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        return _sanitize_location(v)

    @field_validator(
        "total_budget", "restaurant_preference", "dietary_restrictions",
        "meal_budget_per_day", "hotel_preference", "interests",
        "intensity", "events", "schedule_style",
    )
    @classmethod
    def sanitize_text(cls, v: str) -> str:
        return _sanitize_text_field(v)

# Input validation models for API request bodies.
# These enforce input sanitization at the API boundary — rejecting malicious payloads
# (XSS, SQL injection, command injection) before they reach business logic.

import re
from pydantic import BaseModel, Field, field_validator


class LocationRequest(BaseModel):
    """Request body for endpoints that accept a location string."""

    # min_length=2 prevents empty/single-char input; max_length=100 blocks payload stuffing
    location: str = Field(..., min_length=2, max_length=100)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
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


class ItineraryRequest(BaseModel):
    """Request body for the itinerary endpoint — requires location + number of days."""

    location: str = Field(..., min_length=2, max_length=100)
    # ge=1 ensures at least 1 day; le=30 caps trips at 30 days to prevent abuse
    days: int = Field(..., ge=1, le=30)

    @field_validator("location")
    @classmethod
    def sanitize_location(cls, v: str) -> str:
        """Same sanitization rules as LocationRequest — rejects injection payloads."""
        v = v.strip()
        if not re.match(r"^[a-zA-Z\s\-\'.,()À-ɏ]+$", v):
            raise ValueError(
                "Location must contain only letters, spaces, hyphens, "
                "apostrophes, periods, and commas"
            )
        return v

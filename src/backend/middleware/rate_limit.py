# Rate limiter configuration using slowapi.
# Limits the number of API requests per client IP to prevent abuse and DDoS.
# Each endpoint is decorated with @limiter.limit("10/minute") to cap at 10 requests/min per IP.
# When exceeded, returns HTTP 429 Too Many Requests.

from slowapi import Limiter
from slowapi.util import get_remote_address

# key_func=get_remote_address extracts the client IP from the request for per-user throttling
limiter = Limiter(key_func=get_remote_address)

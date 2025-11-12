"""
Rate limiting middleware for FastAPI
Implements token bucket algorithm with in-memory storage
For production, consider using Redis for distributed rate limiting
"""
import time
from collections import defaultdict
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60, requests_per_hour: int = 1000):
        self.rpm_limit = requests_per_minute
        self.rph_limit = requests_per_hour
        # Storage: {client_id: {minute_bucket: (tokens, last_update), hour_bucket: (tokens, last_update)}}
        self.buckets: Dict[str, Dict[str, Tuple[float, float]]] = defaultdict(lambda: {
            'minute': (float(requests_per_minute), time.time()),
            'hour': (float(requests_per_hour), time.time())
        })
        # Cleanup old entries periodically
        self.last_cleanup = time.time()
        
    def _get_client_id(self, request: Request) -> str:
        """Extract client identifier from request"""
        # Try to get real IP from forwarded headers (for proxies/load balancers)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0].strip()
        else:
            client_ip = request.client.host if request.client else "unknown"
        
        # Optionally include user agent for more granular limiting
        # user_agent = request.headers.get("User-Agent", "")
        return client_ip
    
    def _refill_tokens(self, tokens: float, last_update: float, rate: float, max_tokens: float) -> Tuple[float, float]:
        """Refill tokens based on elapsed time"""
        now = time.time()
        elapsed = now - last_update
        new_tokens = min(max_tokens, tokens + elapsed * rate)
        return new_tokens, now
    
    def _cleanup_old_entries(self):
        """Remove old entries to prevent memory leak"""
        now = time.time()
        if now - self.last_cleanup < 3600:  # Cleanup once per hour
            return
        
        # Remove entries older than 2 hours
        cutoff = now - 7200
        to_remove = []
        for client_id, buckets in self.buckets.items():
            if buckets['hour'][1] < cutoff:
                to_remove.append(client_id)
        
        for client_id in to_remove:
            del self.buckets[client_id]
        
        self.last_cleanup = now
        logger.info(f"Rate limiter cleanup: removed {len(to_remove)} old entries")
    
    async def check_rate_limit(self, request: Request) -> None:
        """Check if request should be rate limited"""
        client_id = self._get_client_id(request)
        
        # Skip rate limiting for health checks
        if request.url.path in ["/health", "/readiness"]:
            return
        
        # Periodic cleanup
        self._cleanup_old_entries()
        
        # Get or create buckets
        buckets = self.buckets[client_id]
        
        # Check minute rate limit
        minute_tokens, minute_last_update = buckets['minute']
        minute_rate = self.rpm_limit / 60.0  # tokens per second
        minute_tokens, new_minute_time = self._refill_tokens(
            minute_tokens, minute_last_update, minute_rate, float(self.rpm_limit)
        )
        
        if minute_tokens < 1:
            retry_after = int((1 - minute_tokens) / minute_rate) + 1
            logger.warning(f"Rate limit exceeded for {client_id} (minute limit)")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": f"{self.rpm_limit} requests per minute",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        # Check hour rate limit
        hour_tokens, hour_last_update = buckets['hour']
        hour_rate = self.rph_limit / 3600.0  # tokens per second
        hour_tokens, new_hour_time = self._refill_tokens(
            hour_tokens, hour_last_update, hour_rate, float(self.rph_limit)
        )
        
        if hour_tokens < 1:
            retry_after = int((1 - hour_tokens) / hour_rate) + 1
            logger.warning(f"Rate limit exceeded for {client_id} (hour limit)")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": f"{self.rph_limit} requests per hour",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        # Consume one token from each bucket
        buckets['minute'] = (minute_tokens - 1, new_minute_time)
        buckets['hour'] = (hour_tokens - 1, new_hour_time)
        self.buckets[client_id] = buckets
        
        # Add rate limit info to response headers
        request.state.rate_limit_remaining_minute = int(minute_tokens - 1)
        request.state.rate_limit_remaining_hour = int(hour_tokens - 1)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware to apply rate limiting to all requests"""
    
    def __init__(self, app, rpm: int = 60, rph: int = 1000):
        super().__init__(app)
        self.rate_limiter = RateLimiter(requests_per_minute=rpm, requests_per_hour=rph)
    
    async def dispatch(self, request: Request, call_next):
        await self.rate_limiter.check_rate_limit(request)
        response = await call_next(request)
        
        # Add rate limit headers to response
        if hasattr(request.state, 'rate_limit_remaining_minute'):
            response.headers['X-RateLimit-Remaining-Minute'] = str(request.state.rate_limit_remaining_minute)
        if hasattr(request.state, 'rate_limit_remaining_hour'):
            response.headers['X-RateLimit-Remaining-Hour'] = str(request.state.rate_limit_remaining_hour)
        
        return response

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

import logging
logger = logging.getLogger(__name__)

RATE_LIMIT = 60
REQUESTS_PER_MINUTE = 10

class RateLimiterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request : Request, call_next):
        redis = request.app.state.redis
        
        redis_key = f"rate_limit:{request.client.host}"
        
        used_requests = await redis.get(redis_key)
        
        if used_requests is None:
            counter = await redis.incr(redis_key)
            
            if counter == 1:
                await redis.expire(redis_key, RATE_LIMIT)
            
        else:
            used_requests = int(used_requests)
            if used_requests >= REQUESTS_PER_MINUTE:
                logger.warning(f"Rate limit exceeded for IP {request.client.host}.")
                ttl = await redis.ttl(redis_key)
                return JSONResponse(status_code=429, content={"message": f"Rate limit exceeded for IP {request.client.host}. Try again later in {ttl} seconds."})
            await redis.incr(redis_key)
        
        response = await call_next(request)
        
        
        return response
    
    
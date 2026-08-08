from contextlib import asynccontextmanager
from fastapi import FastAPI
import redis.asyncio as redis
import logging

logger = logging.getLogger(__name__)


REDIS_URL = "redis://localhost:6379/1"

@asynccontextmanager
async def redis_client_lifespan(app: FastAPI):
    
    redis_pool = redis.ConnectionPool.from_url(REDIS_URL,decode_responses=True,encoding="utf-8")
    
    app.state.redis = redis.Redis(connection_pool=redis_pool)
    
    logger.info("Redis client initialized")
    
    yield
    
    await redis_pool.disconnect()
    await app.state.redis.close()
    
    logger.info("Redis client closed")
    
    
    
    
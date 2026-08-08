from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI, Request
from db import get_db
from routes.todo import todo_router
from routes.user import user_router
from routes.auth import auth_router
from lifespan_events import redis_client_lifespan
from middlewares.rate_limiter import RateLimiterMiddleware
load_dotenv()
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
from utils import caching_decorator


app = FastAPI(title="TODO APP", description="Todo app for practice fastapi",version="1.0",lifespan=redis_client_lifespan)

app.add_middleware(RateLimiterMiddleware)

@app.get("/")
@caching_decorator()
async def root(request: Request):
    await asyncio.sleep(2)
    return {"msg" : "Hello World"}

app.include_router(router=auth_router,prefix="/api/auth",tags=["Auth"])
app.include_router(router=todo_router,prefix="/api/todos",tags=["Todo"])
app.include_router(router=user_router, prefix="/api/users",tags=["User"])
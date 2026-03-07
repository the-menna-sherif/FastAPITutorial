from fastapi import FastAPI, HTTPException

from app.schemas import PostCreate, PostResponse
from app.db import create_db_and_tables, get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

# Initialize database -> verify: seeing test.db and acts: creates missing tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()  # Ensure the database and tables are created before the app starts
    yield  # This is where the app runs

# app = FastAPI()  # FastAPI instance without a lifespan function, isn't connected to the database setup, so no fxns in db will execute (creation, etc.)
app = FastAPI(lifespan=lifespan) # FastAPI instance with a lifespan function that creates the database and tables before the app starts

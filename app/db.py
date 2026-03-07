from collections.abc import AsyncGenerator
import uuid 

from sqlalchemy import create_engine
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker ,create_async_engine
from sqlalchemy.orm import DeclarativeBase, relationship

# allow to connect to local db file in current directory
## can connect to another db by changing the DATABASE_URL to the appropriate connection string for that database (e.g., PostgreSQL, MySQL, etc.)
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# data model definition using SQLAlchemy's declarative base
# data model is a class that represents a table in the database, 
# with attributes corresponding to columns in the table
class Post(DeclarativeBase):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid==True), primary_key=True, default=uuid.uuid4) 
from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends

from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

# Initialize database -> verify: seeing test.db and acts: creates missing tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()  # Ensure the database and tables are created before the app starts
    yield  # This is where the app runs

# app = FastAPI()  # FastAPI instance without a lifespan function, isn't connected to the database setup, so no fxns in db will execute (creation, etc.)
app = FastAPI(lifespan=lifespan) # FastAPI instance with a lifespan function that creates the database and tables before the app starts

# Create a new post endpoint
@app.post("/upload")
async def upload_file( # non null args
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session) # dependency injection of db ssn: allows axs to db in this endpoint function (/upload)
):
    # create post instance with its attributes
    post = Post(
        caption=caption,
        url="dummy_url", 
        file_type="photo",
        file_name="dummy_name"
    )

    # add post to db
    session.add(post)
    await session.commit() # commit the transaction to save the post in the database
    await session.refresh(post) # refresh the post instance to get the updated data from the database (e.g., id, created_at)
    
    return post

# Create a new "feed" endpoint
@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session) # dependency injection of db ssn: allows axs to posts
):
    # grab all posts (ordered)
    result = await session.execute(select(Post).order_by(Post.created_at.desc())) # execute a select query to retrieve all posts from the database
    # loop through the result and extract the post instances, return them as a list of posts in the response
    # this is cuz fastapi returns as cursor object, so we need to extract the post instances from the result using a list comprehension
    posts = [row[0] for row in result.all()]

    post_data =[]

    for post in posts:
        post_data.append(
            {
                "id": str(post.id), # convert UUID to string 
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "file_name": post.file_name,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": post_data}

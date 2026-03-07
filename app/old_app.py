from fastapi import FastAPI, HTTPException

from app.schemas import PostCreate, PostResponse
from app.db import create_db_and_tables, get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager

# this had initial tests and basic app

# Initialize database -> verify: seeing test.db and acts: creates missing tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()  # Ensure the database and tables are created before the app starts
    yield  # This is where the app runs

# app = FastAPI()  # FastAPI instance without a lifespan function, isn't connected to the database setup, so no fxns in db will execute (creation, etc.)
app = FastAPI(lifespan=lifespan) # FastAPI instance with a lifespan function that creates the database and tables before the app starts

# container dict for our text posts
# each post has a unique id (int: key) and a dictionary of title and content (strings: value)
text_posts = {
    1: {"title": "New Post", "content": "Cool test post"},
    2: {"title": "Python Tip", "content": "Use list comprehensions for cleaner loops."},
    3: {"title": "Daily Motivation", "content": "Consistency beats intensity every time."},
    4: {"title": "Fun Fact", "content": "The first computer bug was an actual moth found in a Harvard Mark II."},
    5: {"title": "Update", "content": "Just launched my new project! Excited to share more soon."},
    6: {"title": "Tech Insight", "content": "Async IO in Python can massively speed up I/O-bound tasks."},
    7: {"title": "Quote", "content": "Programs must be written for people to read, and only incidentally for machines to execute."},
    8: {"title": "Weekend Plans", "content": "Might finally clean up my GitHub repos... or just play some Minecraft."},
    9: {"title": "Question", "content": "What’s the most underrated Python library you’ve ever used?"},
    10: {"title": "Mini Announcement", "content": "New video drops tomorrow—covering the weirdest Python features!"}
}

# Our READ endpoint to get all text posts
# added an optional (using syntax: = None) query parameter to specify the number of posts to return
# can pass many params (comma separated) 
@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

# Our READ endpoint to get a single text post by id using its path parameter
# added error handling to return a 404 status code if the post with the specified id is not found in our text_posts dictionary
# the response model (PostResponse) ensures that the returned data is structured according to the defined schema, providing consistency in our API responses
@app.get("/posts/{id}")
def get_post(id: str) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)

@app.post("/posts")
# receiving the request body as a pydantic model (PostCreate) which will validate the incoming data
# returning the created post as a PostResponse model which will ensure the response data is structured correctly
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post


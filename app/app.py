from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends

from app.schemas import PostCreate, PostResponse, UserCreate, UserRead, UserUpdate
from app.db import Post, create_db_and_tables, get_async_session

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select

from app.images import imagekit
# from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile

from app.users import auth_backend, fastapi_users, current_active_user

# Initialize database -> verify: seeing test.db and acts: creates missing tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()  # Ensure the database and tables are created before the app starts
    yield  # This is where the app runs

# app = FastAPI()  # FastAPI instance without a lifespan function, isn't connected to the database setup, so no fxns in db will execute (creation, etc.)
app = FastAPI(lifespan=lifespan) # FastAPI instance with a lifespan function that creates the database and tables before the app starts

app.include_router(
    fastapi_users.get_auth_router(auth_backend), # include the authentication router from FastAPI Users, which provides endpoints for user authentication (e.g., login, logout)
    prefix="/auth/jwt", # go to /auth/jwt to access the auth endpoints (e.g., /auth/jwt/login for login)
    tags=["auth"] # tag the auth endpoints with "auth" for documentation purposes
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), # include the registration router from FastAPI Users, which provides endpoints for user registration (e.g., /auth/register)
    prefix="/auth", tags=["auth"])

app.include_router(
    fastapi_users.get_reset_password_router(), 
    prefix="/auth", tags=["auth"])

app.include_router(
    fastapi_users.get_verify_router(UserRead), 
    prefix="/auth", tags=["auth"])

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"])

# Create a new post endpoint
@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        # create a temporary file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(file.filename)[1]
        ) as temp_file:
            temp_file_path = temp_file.name
            file.file.seek(0)
            shutil.copyfileobj(file.file, temp_file)

        # upload to ImageKit
        with open(temp_file_path, "rb") as f:
            upload_result = imagekit.files.upload(
                file=f,
                file_name=file.filename,
                use_unique_file_name=True,
                folder="/posts"
            )

        # check upload success
        if upload_result.response_metadata.http_status_code != 200:
            raise HTTPException(status_code=500, detail="ImageKit upload failed")

        # create post instance
        post = Post(
            caption=caption,
            url=upload_result.url,
            file_type="video" if file.content_type.startswith("video/") else "image",
            file_name=upload_result.name,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

    finally:
        if file:
            file.file.close()

        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except PermissionError:
                pass

    # save to database
    session.add(post)
    await session.commit()
    await session.refresh(post)

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


@app.delete("/posts/{post_id}")
async def delete_post(
    post_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    try:
        post_uuid = uuid.UUID(post_id) # convert the post_id string to a UUID object (for comparing)

        result = await session.execute(select(Post).where(Post.id == post_uuid)) # execute a select query to find the post with the given id
        post = result.scalar_one_or_none() # get the post instance from the result, or None if not found

        if not post:
            raise HTTPException(status_code=404, detail="Post not found") # if post not found, raise a 404 error
        await session.delete(post) # delete the post from the database
        await session.commit() # commit the transaction to save the changes in the database
        return {"success": True} # return a success message in the response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete post: {str(e)}") # if any error occurs during the process, raise a 500 error with the error message
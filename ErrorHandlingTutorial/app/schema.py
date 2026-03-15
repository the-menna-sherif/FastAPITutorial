from pydantic import BaseModel

class Tweet(BaseModel):
    tweet: str
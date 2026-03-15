from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse  
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .schema import Tweet
import re

# rate limiter instance with key function to identify clients by IP address
limiter = Limiter(key_func=get_remote_address) 

# create FastAPI app instance with title
app = FastAPI(title="Simple FastAPI Gateway")

# add rate limiter to app state for access in middleware
app.state.limiter = limiter

# add exception handler for rate limit exceeded errors
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# rou
@app.get("/") # decorator extending my function to be a GET request
def read_root(): # fxn called when root endpoint gets called by GET request
    return {"message": 
            "Hello World!"}

@app.get("/example1") # decorator extending my function to be a GET request
def example1(): # fxn called when /example endpoint gets called by GET request 
  return {"message":
          "My example works!"}

@app.get("/example2")
@limiter.limit("1/second") # apply rate limit to this endpoint
async def example2( # rate limiter mw fxn
   request: Request, 
#    call_next, # takes request and passes to correct path operation, returning reponse
):
    response = {
        "message": "You've reached example2, and haven't been rate limited!"
    }
    return response

# compile regex patterns for common PII types (email, phone, address)
# .compile() pre-compiles the regex for faster matching later
PII_patterns = {
    "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
    "phone": re.compile(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"),
    "address": re.compile(r"\b\d{1,5}\s\w+\s\w+\b"),
}

def contains_pii(text: str) -> bool:
    # check if text contains any PII patterns from above dict
    for _, pattern in PII_patterns.items():
        if pattern.search(text):
            return True
    return False

# this PII checker will use regex-based detection 
@app.middleware("http")
async def checkPII(request: Request, call_next):
    if request.method == "POST":
        body = await request.body()
        body_str = body.decode("utf-8")

        if contains_pii(body_str):
                # Reject request if PII detected
                raise HTTPException(status_code=400, detail="PII detected in tweet!")
    response = await call_next(request)

    return response

# this endpoint will be my implementation of PII handling

@app.post("/tweet")
async def tweet(request: Tweet,
):
   tweet = await checkPII(request)
   return tweet
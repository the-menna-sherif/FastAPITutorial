from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse  
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

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
   call_next, # takes request and passes to correct path operation, returning reponse
):
    response = await call_next(request)
    return response


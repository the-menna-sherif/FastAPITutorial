# Progress documentation



Will be tracking where I stopped here.

1. Create & activate python venv using vscode PS terminal:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. Create a basic API gateway:

# Error documentation

1. Running my main.py:
Command:
> PS > python .\app\main.py

Error:
```
ERROR: Error loading ASGI app. Could not import module "app.app".
```

> Fix: moving the main.py outside app.py. Used a 'flat structure' which allows uvicorn to see main immediately as I run everything from the the project folder. No need for an __init__.py.

2. Not getting any 429s after running my test.py:
Command:
> PS > python test.py

Error/ output: 
```
Request 1: 200 {"message":"Hello World!"}
Request 2: 200 {"message":"Hello World!"}
Request 3: 200 {"message":"Hello World!"}
Request 4: 200 {"message":"Hello World!"}
Request 5: 200 {"message":"Hello World!"}
```

> Fix: Path parameter (endpoint) my test.py was testing wasn't the one rate limited. Fixed local url parameter to: url = "http://127.0.0.1:8000/example2" instead of just the localhost.

3. Not getting any 429s after running my test.py:
Command:
> PS > python test.py

Error/ output: 
```
Request 1: 200 {"message":"Hello World!"}
Request 2: 200 {"message":"Hello World!"}
Request 3: 200 {"message":"Hello World!"}
Request 4: 200 {"message":"Hello World!"}
Request 5: 200 {"message":"Hello World!"}
```
> Fix: the rate limiter was 1/second, the limiter saw them as one “instant” and allowed them. Added a delay between the requests:
```
await asyncio.sleep(0.05)
```

4. The below error when testing:
Command:
> PS > python test.py

Error:
```
Request 1: 422 {"detail":[{"type":"missing","loc":["query","call_next"],"msg":"Field required","input":null}]}
Request 2: 422 {"detail":[{"type":"missing","loc":["query","call_next"],"msg":"Field required","input":null}]}
Request 3: 422 {"detail":[{"type":"missing","loc":["query","call_next"],"msg":"Field required","input":null}]}
Request 4: 422 {"detail":[{"type":"missing","loc":["query","call_next"],"msg":"Field required","input":null}]}
Request 5: 422 {"detail":[{"type":"missing","loc":["query","call_next"],"msg":"Field required","input":null}]}
```

> Fix: I had mixed my approaches. My initial approach was to use a middleware layer. I later swapped to slowapi but forgot to alter my /example2 endpoint (still contained call_next : global http request interception and routing).
 

# References:

Creating the basic gateway:
https://www.geeksforgeeks.org/python/creating-first-rest-api-with-fastapi/

Rate Limiting using slowapi:
https://github.com/laurentS/slowapi
https://slowapi.readthedocs.io/en/stable/#fastapi

Error handling:
https://fastapi.tiangolo.com/tutorial/handling-errors/?h=handling

Cool logic diagram:
https://thedkpatel.medium.com/rate-limiting-with-fastapi-an-in-depth-guide-c4d64a776b83

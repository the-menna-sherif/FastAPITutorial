# Error tracking & debugging notes:

1- This site can't be reached when opening the URL on browser:

REZ: change from 0.0.0.0:8000 to either localhost:8000 or 127.0.0.1:8000

Backend & logs:
<img width="1351" height="265" alt="image" src="https://github.com/user-attachments/assets/6cf999cf-e0fb-4bd2-a6ef-8845d633af64" />
Frontend:

<img width="218" height="90" alt="image" src="https://github.com/user-attachments/assets/b7f49aa9-37e0-462d-aa82-c1c13058002a" />

## Docs and trying functions from the UI:

http://localhost:8000/redoc 

<img width="473" height="462" alt="image" src="https://github.com/user-attachments/assets/bbf4ff5b-8b50-4e92-8946-ffdbc830a71e" />

or

http://localhost:8000/docs

```
# create a test endpoint/ resource: GET (flow: declarator > fxn) 
@app.get("/hello-world")
def hello_world():
    # return any data in either a dictionary (below) or a pydantic object
    return {"message": "Hello World"}
```

<img width="477" height="518" alt="image" src="https://github.com/user-attachments/assets/651670d5-b6e1-4635-9c91-bc773b0f3d85" />


or

http://localhost:8000/<fxn name>

### GET functions

First is a generic GET to grab all the posts, just given a path. Second is a more granular one to get a *specific* post using the path parameter id.

<img width="473" height="350" alt="image" src="https://github.com/user-attachments/assets/d1d11cac-cd96-4bb7-a10d-8b4d74e530eb" />

#### Added exception handling to GET functions using the HTTPException library:

UI:

<img width="458" height="465" alt="image" src="https://github.com/user-attachments/assets/e8d4da24-3a2a-4c95-9b53-a0123cfc258a" />

Logs:

<img width="506" height="156" alt="image" src="https://github.com/user-attachments/assets/1b2036ac-5164-4f5f-a506-3c6c94082067" />

#### Added query parameter limit (limit returned posts):

- Failed at first as the code applies a list operation to dict (returning a server error as the code is the API server)

  <img width="461" height="436" alt="image" src="https://github.com/user-attachments/assets/b6f8654d-f656-4975-a2f0-ac061eb8f4de" />

  Code before:

  ```
  text_posts = {
    "1": {"title": "New Post", "content": "Cool test post"},
  }
return text_posts[:limit]
  ```


  Code after:

  ```
  text_posts = {
    "1": {"title": "New Post", "content": "Cool test post"},
  }
return list(text_posts.values())[:limit]
  ```


Error logged:
  File "C:<path>\.venv\Lib\site-packages\anyio\_backends\_asyncio.py", line 986, in run     
    result = context.run(func, *args)
  File "C:<path>\FastAPITutorial\app\app.py", line 31, in get_all_posts
    return text_posts[:limit]
           ~~~~~~~~~~^^^^^^^^
KeyError: slice(None, 5, None)

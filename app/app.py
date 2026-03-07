from fastapi import FastAPI

app = FastAPI()

# Create endpoint & method

# create a   for the endpoint 
@app.get("/hello-world")
def hello_world():
    # return any data in either a dictionary (below) or a pydantic object
    return {"message": "Hello World"}
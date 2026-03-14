from fastapi import FastAPI

app = FastAPI()

# decorator extending my function to be a GET request
@app.get("/")
def read_root():
    return {"message": 
            "Hello World!"}

@app.get("/")
def example1():
  return {"message":
          "My example works!"}
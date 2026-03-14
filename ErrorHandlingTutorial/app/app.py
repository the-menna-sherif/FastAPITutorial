from fastapi import FastAPI

app = FastAPI(title="Simple FastAPI Gateway")


@app.get("/") # decorator extending my function to be a GET request
def read_root(): # fxn called when root endpoint gets called by GET request
    return {"message": 
            "Hello World!"}

@app.get("/example") # decorator extending my function to be a GET request
def example1(): # fxn called when /example endpoint gets called by GET request 
  return {"message":
          "My example works!"}



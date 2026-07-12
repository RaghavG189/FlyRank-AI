from fastapi import FastAPI #import fastapi
from pydantic import BaseModel #import basemodel

app = FastAPI() #create an instance (app) of the class FastAPI


@app.get("/") #Define path operation decorator - tells function below to handle all requests that go to "/"
#'.get' is the HTTP method

#Define a path operation function
async def root():
    return {"Data": "This is a test."}


#Create Class
class Description(BaseModel):
    name : str
    age : int

@app.post("/descriptions/") #Define path operation decorator
#Define function 
async def create_item(description : Description):
    return description

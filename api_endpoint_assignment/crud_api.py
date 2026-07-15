from fastapi import FastAPI #import fastapi
from pydantic import BaseModel #import basemodel

#create instance of fastapi
app = FastAPI()

#define path operation decorator
@app.get('/greeting')

#define path operation function
async def greet():
    return {"message": "hello server"}



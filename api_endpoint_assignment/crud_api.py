from fastapi import FastAPI #import fastapi
from pydantic import BaseModel #import basemodel

#create instance of fastapi
app = FastAPI()


#STAGE 0
#define path operation decorator
@app.get('/greeting')

#define path operation function
async def greet():
    return {"message": "hello server"}


#STAGE 1
@app.get('/')

async def describe():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get('/health')

async def status():
    return {"status": "ok"}


#Stage 2

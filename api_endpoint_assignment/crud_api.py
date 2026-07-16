from fastapi import FastAPI, HTTPException #import fastapi and HTTPException
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
tasks = [
{"task_id": 1, "title": "vaccumming", "done": True}, 
{"task_id": 2, "title": "laundry", "done": False}, 
{"task_id": 3, "title": "dishes", "done": True}
]


@app.get('/tasks')

async def get_tasks():
    return tasks


@app.get("/tasks/{task_id}")

async def get_task(task_id: int):
    for task in tasks:
        if task["task_id"] == task_id:
            return task
    
    raise HTTPException(status_code=404, detail={"error": f"task {task_id} not found"})


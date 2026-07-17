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


#Stage 3
#declare class
class Task(BaseModel):
    id: int | None = None
    title: str | None = None
    done : bool | None = None

@app.post('/tasks', status_code=201)

async def create_task(task:Task):
    task_dict = task.model_dump()
    if task.title is not None and task.title.strip() != "":
        if task.id is None and task.done is None:

                task_dict.update({"id": len(tasks) + 1})
                task_dict.update({"done": False})
        
        tasks.append(task_dict)

        return task_dict
    
    raise HTTPException(status_code=400, detail="Title is either missing or empty.")


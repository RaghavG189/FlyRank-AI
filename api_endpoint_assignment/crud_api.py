from fastapi import FastAPI, HTTPException #imports FastAPI and HTTPException
from pydantic import BaseModel #import basemodel

#create instance of fastapi for endpoints
app = FastAPI()


#STAGE 0
#defines path operation decorator
@app.get('/greeting')

#defines path operation function
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

async def get_tasks(): #Returns list of all tasks
    return tasks


@app.get("/tasks/{task_id}")

async def get_task(task_id: int): #Returns specific task by ID
    for task in tasks:
        if task.get("task_id") == task_id:
            return task
    
    raise HTTPException(status_code=404, detail={"error": f"task {task_id} not found"}) #Raises 404 if id not valid


#Stage 3
#declare class
class Task(BaseModel):
    task_id: int | None = None
    title: str | None = None
    done : bool | None = None

#get lastest_id
if len(tasks) == 0:
    latest_id = 0
else:
    max_id = 0
    for task in tasks:
        max_id = max(max_id, task.get("task_id"))

    latest_id = max_id


@app.post('/tasks', status_code=201)

async def create_task(task:Task):
    task_dict = task.model_dump() #Get model of class with values

    if task.title is not None and task.title.strip() != "": #Checks if title value is valid - not null and ""
        if task.done is None:

            #retieve global variable and update
            global latest_id
            latest_id += 1

            task_dict.update({"task_id": latest_id})
            task_dict.update({"done": False})
        
        global tasks
        tasks.append(task_dict) #append new task to tasks list

        return task_dict
    
    raise HTTPException(status_code=400, detail="Title is either missing or empty.") #Raise 400 if title is missing/invalid


#Stage 4
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task:Task):
    task_dict = None

    for t in tasks: #get correct task from list of tasks based on task id
        if t.get("task_id") == task_id: 
            task_dict = t
    
    if task_dict is None:
        raise HTTPException(status_code=404, detail=f"Unknown ID: Could not find task {task_id}") #Raise 404 if task not found
    

    if (task.title is None or task.title.strip() == "") and task.done is None:
        raise HTTPException(status_code=400, detail="Invalid/missing title and done status") #Raise 400 if both title and done values are missing

    if task.title is not None and task.title.strip() != "":
        task_dict['title'] = task.title #change title to user given value
    
    if task.done is not None:
        task_dict['done'] = task.done #Change done to user given value

    return task_dict
    
@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id:int):
    
    for index, task in enumerate(tasks): #Find the task
        if task.get("task_id") == task_id:
            tasks.pop(index) #Remove from list

            return None
        
    raise HTTPException(status_code=404, detail="Unknown ID") #Raise 404 if task was not found given ID

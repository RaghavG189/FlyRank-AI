from fastapi import APIRouter
from pydantic import BaseModel
import src.services.tasks_services as s


router = APIRouter(tags=['Tasks']) #Creates router object


#Get endpoint that retrieves all tasks using filtering
@router.get('/tasks')
def get_tasks(done:bool | None = None, title:str | None = None):
    filtered_tasks = s.list_tasks(done, title)

    return filtered_tasks


#Get endpoint that retrieves single task by user id
@router.get('/tasks/{task_id}')
def get_task(task_id: int):

    task = s.task_id(task_id)

    return task


class Createtask(BaseModel): #pydantic class for POST endpoint defined to check user inputs
    title: str
    done: bool = False

#Post endpoint that creates a task
@router.post('/tasks', status_code=201)
def create_task(createtask:Createtask):

    output = s.make_task(createtask.title, createtask.done)

    return output


class Updatetask(BaseModel): #pydantic class for PUT endpoint defined to check user inputs
    task_id: int 
    title: str | None = None
    done: bool | None = None

#PUT endpoint that updates a task
@router.put('/tasks/{task_id}')
def update_task(updatetask:Updatetask):

    updated_task = s.update_task(updatetask.task_id, updatetask.title, updatetask.done)

    return updated_task


#DELETE endpoint that deletes a task given task id
@router.delete('/tasks/{task_id}', status_code=204)
def delete_task(task_id:int):

    output = s.deleted_task(task_id)

    return output

    
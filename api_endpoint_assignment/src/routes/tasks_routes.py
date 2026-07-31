from fastapi import APIRouter
from pydantic import BaseModel
import src.services.tasks_services as s


router = APIRouter()



@router.get('/tasks')
def get_tasks(done:bool | None = None, title:str | None = None):
    filtered_tasks = s.list_tasks(done, title)

    return filtered_tasks


@router.get('/tasks/{task_id}')
def get_task(task_id: int):

    task = s.task_id(task_id)

    return task


class Createtask(BaseModel):
    title: str
    done: bool = False

@router.post('/tasks', status_code=201)
def create_task(createtask:Createtask):

    output = s.make_task(createtask.title, createtask.done)

    return output


class Updatetask(BaseModel):
    task_id: int 
    title: str | None = None
    done: bool | None = None

@router.put('/tasks/{task_id}')
def update_task(updatetask:Updatetask):

    updated_task = s.update_task(updatetask.task_id, updatetask.title, updatetask.done)

    return updated_task


@router.delete('/tasks/{task_id}', status_code=204)
def delete_task(task_id:int):

    output = s.deleted_task(task_id)

    return output

    
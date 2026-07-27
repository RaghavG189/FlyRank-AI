import src.repositories.tasks_repository as repo 
from src.errors import NotFoundError, ValidationError




def list_tasks(done:bool, search:str):

    result = repo.get_tasks()

    #Extra: Filter by done value
    if (done != None):
        if (done is not True and done is not False):
            raise ValidationError("done must be true or false.")


        result = [task for task in result if task['done'] == done]

    #Extra: filter by title
    if (search != None):
        word = search.strip()

        if word == "":
            raise ValidationError("title must not be empty.")

        word = word.lower()

        result = [task for task in result if task['title'] == search]

    return result


def task_id(task_id: int):

    task = repo.get_task_id(task_id)

    if task == None:
        raise NotFoundError(f"Task {task_id} was not found.")

    return task


def make_task(title:str, done:bool=False):

    if title is None or title.strip() == "":
        raise ValidationError("Title cannot be empty.")

    return repo.create_task(title, done)


def update_task(task_id: int, title:str, done:bool):

    updates = {}

    if title is None and done is None:
        raise ValidationError("Request body must have title and/or done.")

    if title:
        if title.strip() == "":
            raise ValidationError("Title cannot be empty.")

        updates['title'] = title

    if done:
        updates['done'] = done

    updated_task = repo.update_task(task_id, updates)

    if updated_task is None:
        raise NotFoundError(f"Task {task_id} was not found.")

    return updated_task
    

def deleted_task(task_id:int):
    deleted = repo.delete_task(task_id)

    if deleted is False:
        raise NotFoundError(f"Task {task_id} was not found.")

    return deleted
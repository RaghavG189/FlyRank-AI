tasks = [
{"task_id": 1, "title": "vaccumming", "done": True}, 
{"task_id": 2, "title": "laundry", "done": False}, 
{"task_id": 3, "title": "dishes", "done": True}
]

current_task_id = 0 if len(tasks) == 0 else max([task['task_id'] for task in tasks])


def get_tasks():
    return tasks


def get_task_id(task_id: int):

    for task in tasks:
        if task["task_id"] == task_id:
            return task

    return None


def create_task(title:str, done:bool):

    global current_task_id
    current_task_id += 1

    task = {
        "task_id": current_task_id,
        "title":title,
        "done":done
    }

    tasks.append(task)

    return task


def update_task(task_id: int, updates:dict):

    for task in tasks:
        if task["task_id"] == task_id:
            task.update(updates)
            return task
    
    return None


def delete_task(task_id:int):

    for index, task in enumerate(tasks):
        if task["task_id"] == task_id:
            tasks.pop(index)
            return True

    return False

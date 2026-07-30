import sqlite3 as sq


con = sq.connect("tasks.db", check_same_thread=False)


con.row_factory = sq.Row

cur = con.cursor()

#Creates task table to store data
create_table_query = "CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, done BOOLEAN CHECK (done in (0, 1)))"
cur.execute(create_table_query)

#Insert example tasks if table empty
sample_query = '''INSERT INTO tasks(title, done)
SELECT 'dishes', 1 WHERE NOT EXISTS (SELECT 1 FROM tasks LIMIT 1)
UNION ALL
SELECT 'laundry', 0 WHERE NOT EXISTS (SELECT 1 FROM tasks LIMIT 1)
UNION ALL
SELECT 'cooking', 1 WHERE NOT EXISTS (SELECT 1 FROM tasks LIMIT 1);
'''
cur.execute(sample_query)
con.commit()



def close_connection():

    cur.close()
    con.close()


def get_tasks():

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    return tasks


def get_task_id(task_id: int):

    cur.execute("SELECT * FROM tasks where id = ?", (task_id,))
    task = cur.fetchone()

    return task
    

def create_task(title:str, done:bool):

    cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, done))
    con.commit()

    cur.execute("SELECT * FROM tasks where title = ? AND done = ?", (title, done))
    task = cur.fetchone()
    
    return task

'''
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
'''
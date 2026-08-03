#import sqlite3 for database usage
import sqlite3 as sq

#Connect to the database - tasks.db
con = sq.connect("tasks.db", check_same_thread=False) #check_same_thread set to false allowing multiple threads


con.row_factory = sq.Row #Converts database rows into dictionary style format 


cur = con.cursor() #Cursor object for execute, fetchone, fetchall commands


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


#Function called in main to close database connection and cursor
def close_connection():

    cur.close()
    con.close()


#Function that gets all tasks from database
def get_tasks():

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    return tasks


#Function that gets specific task by id
def get_task_id(task_id: int):

    cur.execute("SELECT * FROM tasks where id = ?", (task_id,))
    task = cur.fetchone()

    return task
    

#Function that creates a task and stores in database
def create_task(title:str, done:bool):

    cur.execute("INSERT INTO tasks (title, done) VALUES (?, ?)", (title, done))
    con.commit()

    #Retrieve created task to send back to user
    new_task_id = cur.lastrowid
    cur.execute("SELECT * FROM tasks where id = ?", (new_task_id,))
    task = cur.fetchone()
    
    return task


#Function that updates task in database given user updates
def update_task(task_id: int, updates:dict):

    cur.execute("UPDATE tasks SET title = COALESCE(?, title), done = COALESCE(?, done) WHERE id = ?", (updates.get('title'), updates.get('done'), task_id))
    con.commit()

    #Checks if data was found, updated and then returns
    if cur.rowcount > 0:
        cur.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        task = cur.fetchone()

        return task

    #If data never found then return none to raise error
    return None


#Function that deletes task from database given task id
def delete_task(task_id:int):

    cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    con.commit()

    #if changes not identified return false to raise error
    if cur.rowcount == 0:
        return False
    
    return None

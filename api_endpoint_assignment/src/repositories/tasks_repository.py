#import psycopg to connect to database
import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

load_dotenv()

#Retrieve values located in .env file
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
db = os.environ["POSTGRES_DB"]

#Create the connection URL given variables
url = f"postgres://{user}:{password}@{host}:{port}/{db}"

#Establish connection object
con = psycopg.connect(url, row_factory=dict_row)

#Create cursor object
cur = con.cursor()

#Create tasks table if not already present
cur.execute("""CREATE TABLE IF NOT EXISTS tasks(id serial PRIMARY KEY, title text, done boolean)""")

#Seed 3 example tasks if table empty
cur.execute("""INSERT INTO tasks(title, done)
SELECT * FROM (
    VALUES
        ('dishes', true),
        ('laundry', false),
        ('cleaning', false)
) as sample_tasks
WHERE NOT EXISTS (
SELECT 1 from tasks
);
""")
con.commit() #Commit changes to take effect



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

    cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()

    return task
    

#Function that creates a task and stores in database
def create_task(title:str, done:bool):

    cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *", (title, done))
    con.commit()

    task = cur.fetchone()
    
    return task


#Function that updates task in database given user updates
def update_task(task_id: int, updates:dict):

    cur.execute("UPDATE tasks SET title = COALESCE(%s, title), done = COALESCE(%s, done) WHERE id = %s", (updates.get('title'), updates.get('done'), task_id))
    con.commit()

    #Checks if data was found, updated and then returns
    if cur.rowcount > 0:
        cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cur.fetchone()

        return task

    #If data never found/changed then return none to raise error
    return None


#Function that deletes task from database given task id
def delete_task(task_id:int):

    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    con.commit()

    #if changes not identified return false to raise error
    if cur.rowcount == 0:
        return False
    
    return None

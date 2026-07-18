CURD API TASK MANAGER

What this is: This is a task manager that follows the full CURD cycle. Using GET, POST, PUT, and DELETE endpoints, you can get, create, change, and delete tasks of your liking. 

How to install: Inside the "api_endpoint_assignment" folder is a "requirements.txt" file that has all the libraries you need to run the code - FastAPI, Pydantic, Uvicorn, Swagger UI.
To install the packages, run the following command in the terminal: "pip install -r requirements.txt"

How to Run: To run the code, type "fastapi dev crud_api.py" in the terminal
When the server starts, open another terminal preferably command prompt and enter the following code
to test an endpoint such as GET
Example command: "curl.exe -i http://localhost:8000/tasks" This command will retrieve all current tasks


All Endpoints:
|----------|--------------------------------|-----------------|
|Endpoint  |	Description	                  | Example Command |
|----------|--------------------------------|-----------------|
|  GET     |   Retrieves data from server   | curl.exe -i http://localhost:8000/tasks
|  POST	   |   Sends data to the server     | curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"laundry\"}"
|  PUT	   |   Replace a resource identified| curl.exe -i -X PUT http://localhost:8000/tasks{task_id} -H "Content-Type: application/json" -d "{\"done\":true}"        
|          |   with a given URL             |         
|  DELETE  |   Removes Resource from server | curl.exe -i -X DELETE http://localhost:8000/tasks/{task_id}    


Example output using command:
Running the command "curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"laundry\"}"" will output the following:
---------------------------------------------
HTTP/1.1 201 Created
date: Sat, 18 Jul 2026 19:12:39 GMT
server: uvicorn
content-length: 43
content-type: application/json

{"task_id":4,"title":"mowing","done":false}
---------------------------------------------
The server will assign a task_id for you and set done to false. You can add your own value for "done".


Swagger UI: If you are interested in using Swagger UI, a link will be given to you "http://127.0.0.1:8000/docs" when you start the server.
Screenshot of UI:
<img width="2198" height="680" alt="Screenshot 2026-07-18 142736" src="https://github.com/user-attachments/assets/7e3fa51a-d2b1-4910-a4c4-d98a314d048d" />

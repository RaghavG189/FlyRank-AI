# CURD API Task Manager

A simple FastAPI task manager that supports the full CRUD cycle using GET, POST, PUT, and DELETE endpoints. You can retrieve, create, update, and delete tasks using the provided API.

## Features

- GET `/tasks` to list all tasks
- POST `/tasks` to create a new task
- PUT `/tasks/{task_id}` to update an existing task
- DELETE `/tasks/{task_id}` to remove a task
- Optional SQLite persistence with `tasks.db`
- Swagger UI available at `/docs`

## Run the server

When downloading the files make sure to replace the placeholder values in .env.example for .env

Enter docker compose up to run the application. This will install all the dependencies, project files, and will start the server.

When the server starts, the API is available at `http://127.0.0.1:8000`. Change the given link http://0.0.0.0:8000 to http://127.0.0.1:8000

## Test the API

Use `curl.exe` or your preferred HTTP client.

Example:

```bash
curl.exe -i http://localhost:8000/tasks
```

## Swagger UI

Open the browser and go to:

```text
http://127.0.0.1:8000/docs
```

Screenshot of UI:

<img width="2198" height="680" alt="Swagger UI Screenshot" src="https://github.com/user-attachments/assets/7e3fa51a-d2b1-4910-a4c4-d98a314d048d" />

## Endpoints

| Endpoint | Description | Example Command |
| --- | --- | --- |
| `GET /tasks` | Retrieve all tasks | `curl.exe -i http://localhost:8000/tasks` |
| `POST /tasks` | Create a new task | `curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"laundry\"}"` |
| `PUT /tasks/{task_id}` | Update a task's fields | `curl.exe -i -X PUT http://localhost:8000/tasks/{task_id} -H "Content-Type: application/json" -d "{\"done\":true}"` |
| `DELETE /tasks/{task_id}` | Delete a task | `curl.exe -i -X DELETE http://localhost:8000/tasks/{task_id}` |

## Example response

Running this command:

```bash
curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"mowing\"}"
```

Produces output similar to:

```http
HTTP/1.1 201 Created
Date: Sat, 18 Jul 2026 19:12:39 GMT
Server: uvicorn
content-length: 43
content-type: application/json

{"task_id":4,"title":"mowing","done":false}
```

The server assigns a `task_id` automatically and defaults `done` to `false` unless otherwise specified.


## Notes

Example SQL query used during testing:

```sql
DELETE FROM tasks WHERE done = 1;
```

If no rows are returned, that means all tasks were already marked as `done = 1`.
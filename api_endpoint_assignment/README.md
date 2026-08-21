# CURD API Task Manager

A simple FastAPI task manager that supports the full CRUD cycle using GET, POST, PUT, and DELETE endpoints. You can retrieve, create, update, and delete tasks using the provided API.

## Features

- GET `/tasks` to list all tasks
- POST `/tasks` to create a new task
- PUT `/tasks/{task_id}` to update an existing task
- DELETE `/tasks/{task_id}` to remove a task
- Swagger UI available at `/docs`

## How to setup .env variables

When downloading all project files, you will be given 8 variables in your .env.example. Change .env.example to .env and for each variable:

POSTGRES_USER = Set this to your chosen username
POSTGRES_PASSWORD = Set this to your chosen postgres password
POSTGRES_DB = Set this to the name you set for the db
POSTGRES_HOST = Set this to "localhost"
POSTGRES_PORT = Set this to 5432

SUPABASE_URL = You will enter the supabase URL for your supabase project
SUPABASE_KEY = You will enter the anon key in your supabase project
PORT = You can set this to either 3000 or 8000


## Run the server

When downloading the files make sure to replace the placeholder values in .env.example for .env

Type "docker compose up" to run the application or "docker compose up --build" if you made file changes. This will install all the dependencies, project files, and will start the server.

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

## TASK Endpoints

| Endpoint | Description | Example Command |
| --- | --- | --- |
| `GET /tasks` | Retrieve all tasks | `curl.exe -i http://localhost:8000/tasks` |
| `POST /tasks` | Create a new task | `curl.exe -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d "{\"title\":\"laundry\"}"` |
| `PUT /tasks/{task_id}` | Update a task's fields | `curl.exe -i -X PUT http://localhost:8000/tasks/{task_id} -H "Content-Type: application/json" -d "{\"done\":true}"` |
| `DELETE /tasks/{task_id}` | Delete a task | `curl.exe -i -X DELETE http://localhost:8000/tasks/{task_id}` |

## AUTH API Reference

| Method | Endpoint | Description | Auth Required | Example Command |
| --- | --- | --- | --- | --- |
| `POST` | `/auth/signup` | Create a new user account | No | `curl.exe -i -X POST http://localhost:8000/auth/signup -H "Content-Type: application/json" -d "{\"email\":\"user@example.com\",\"password\":\"secret\"}"` |
| `POST` | `/auth/login` | Authenticate a user and return access and refresh tokens | No | `curl.exe -i -X POST http://localhost:8000/auth/login -H "Content-Type: application/json" -d "{\"email\":\"user@example.com\",\"password\":\"secret\"}"` |
| `GET` | `/protected/profile` | Return the authenticated user's profile | Yes, bearer token | `curl.exe -i http://localhost:8000/protected/profile -H "Authorization: Bearer <access_token>"` |
| `POST` | `/auth/logout` | Log the authenticated user out of all sessions | Yes, bearer token | `curl.exe -i -X POST http://localhost:8000/auth/logout -H "Authorization: Bearer <access_token>"` |
| `GET` | `/public/info` | Return public API information | No | `curl.exe -i http://localhost:8000/public/info` |

## Swagger UI Inputting Token for Authentication





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
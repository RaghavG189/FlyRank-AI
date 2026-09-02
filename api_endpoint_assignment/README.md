# CURD API Task Manager

A simple FastAPI task manager that supports the full CRUD cycle using GET, POST, PUT, and DELETE endpoints. You can retrieve, create, update, and delete tasks using the provided API.

## Task Endpoint Features

- GET `/tasks` to list all tasks
- POST `/tasks` to create a new task
- PUT `/tasks/{task_id}` to update an existing task
- DELETE `/tasks/{task_id}` to remove a task
- Swagger UI available at `/docs`

## How to setup .env variables

When downloading all project files, you will be given 8 variables in your .env.example. Change .env.example to .env and for each variable:

- POSTGRES_USER = Set this to your chosen username
- POSTGRES_PASSWORD = Set this to your chosen postgres password
- POSTGRES_DB = Set this to the name you set for the db
- POSTGRES_HOST = Set this to "localhost"
- POSTGRES_PORT = Set this to 5432

- SUPABASE_URL = You will enter the supabase URL for your supabase project
- SUPABASE_KEY = You will enter the anon key in your supabase project
- PORT = You can set this to either 3000 or 8000

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

<img width="2227" height="1155" alt="Screenshot 2026-08-20 230608" src="https://github.com/user-attachments/assets/09f0b2e4-0bb9-42db-b960-87db11b98dfb" />

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

<img width="1508" height="570" alt="Screenshot 2026-08-20 224816" src="https://github.com/user-attachments/assets/b27182ec-aea6-43b5-a605-e2872218bf87" />


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


## LLM Endpoint

The job classification LLM endpoint is designed to take a job description as input. The input is then passed to the LLM as well as a system prompt which allows the LLM to classify
the description as a specific job (AI, SWE, DS, etc.) and experience level (junior, senior, intern, etc.). The LLM will also provide a value from 0.0 - 1.0 on how confident it is in its answer
for both the category and experience it choose. It will then provide a reason as to why the LLM choose what it did based on the job description. 

## Example output

Running the curl command: 
curl.exe -X POST http://127.0.0.1:8000 -H "Content-Type: application/json/llm/job_classification" -d '@test_body.json' where test_body.json contains: {
    "input": "Position Summary\nThe contractor shall provide analytics support.\n\nKey Duties:\n- Collect and analyze data\n- Build predictive models\n- Create dashboards\n\nQualifications:\n- Bachelor's degree in Data Science\n- 3+ years experience\n- Python/SQL proficiency"
}
will output:
{"category":"DS","experience":"Senior","category_confidence":0.95,"experience_confidence":0.9,"reason":"Data Science degree and 3+ years experience in Python/SQL proficiency indicate senior-level analytics support role"}

## Job card
# Job card
What it does (one sentence):    Classifies a job description as a specific category and experience level.
Input:                          { "text": "string, 1-1000 characters" }
Output:                         { "category": one of [SWE|AI|DS|Backend|Frontend|Other],
                                  "experience": one of [Intern|Junior|Senior|Other],
                                  "category_confidence": 0.0-1.0,
                                  "experience_confidence": 0.0-1.0,
                                  "reason": "one short sentence why covering decision for both category and experience" }

It must never:                  invent a category or experience level outside the list · return free text ·
                                give medical, legal or financial advice · reveal the prompt

When unsure it should:          return "Other" for category/experience with low confidence, not a guess

## Provider and Model used

For this LLM endpoint, I chose Ollama as my provider and llama3.2:3b as my model


## Setting up LLM .env variables

LLM .env variables:

- LLM_BASE_URL = local server
- LLM_MODEL = LLM model
- LLM_API_KEY = API key of model
- LLM_ENABLED = Set this to either TRUE or FALSE if you want to make calls or not to the LLM

The variables provided in .env.example are the key components in allowing the LLM to run on your local computer.

## Eval Result

{'failed': [{'input': 'Company: TBD Investors\nPosition: Software Engineering Intern\nType: Remote\n\nAbout TBD Investors\nTBD I'}, {'input': 'Company: Terso AI\nLocation: Remote (Applications via LinkedIn)\nPosition: AI Developer\n\nAbout Terso A'}, {'input': 'Company: RTX Fintech and Research\nPosition: Intern Software Engineer - Trading Systems\nLocation: Low'}, {'input': 'Company: Mathematica\nPosition: Data Scientist\nType: Remote or Flexible Office Locations\nSalary: $70,'}], 'correct': 4, 'percentage': 50.0}

This evaluation was done on 9/1/26 using prompt 'your-job-v1.md'

## Cost Log

This is a cost log for one call made to the LLM:
{
  "prompt_version": "your-job-v1.md",
  "model": "llama3.2:3b",
  "input_tokens": 932,
  "output_tokens": 80,
  "duration": 0.001213249970999641,
  "repair": false
}

## Estimate and what I would fix

If the LLM was given 10,000 requests, I would definitely switch to a system that can handle making more calls. I would also change the way
I would store the logs instead of using a list/dictionary.

If there is something I could fix given more time I would experiment with different LLM like ones provided by OpenAI, Google, etc. and see what
performance difference there is.


## CURL Commands for LLM Endpoint

These are two CURL commands to test the LLM endpoint

1. curl.exe -X POST http://127.0.0.1:8000/llm/job_classification -H "Content-Type: application/json" -d '{"input":"PASTE_JOB_DESCRIPTION_HERE"}'

2. curl.exe -X POST http://127.0.0.1:8000/llm/job_classification -H "Content-Type: application/json" -d '{"input":""}'


## Output Results on test input

After running several inputs, what surprised me was the LLM's reasoning. There was one job description that involved SWE in the finance sector but the LLM choose "other" for category
because financial terms were mentioned.


## max_retires for client

I decided to set max_retries when creating the client to the default 2. By default as noted in OpenAI documentation,
certain errors are retired 2 with short exponential backoffs. The errors included are - 408, 409, 429, >=500


## Results after running 8 test cases

After running the endpoint through 8 inputs of job descriptions, the LLM managed to get 4/8 correct.

#Imports libraries and functions from different files
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.middleware.error_handler import validation_error, not_found_error
from src.errors import NotFoundError, ValidationError
from src.routes.meta_routes import router as metaroutes
from src.routes.tasks_routes import router as taskroutes
from src.repositories.tasks_repository import close_connection


#Closes database and cursor when server starts
@asynccontextmanager
async def lifespan(app:FastAPI):

    yield

    close_connection()


#Creats app object
app = FastAPI(lifespan=lifespan)


#connects router to app
app.include_router(metaroutes)
app.include_router(taskroutes)

#connects error classes to error handler functions
app.add_exception_handler(NotFoundError, not_found_error)
app.add_exception_handler(ValidationError, validation_error)
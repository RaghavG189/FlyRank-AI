from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.middleware.error_handler import validation_error, not_found_error
from src.errors import NotFoundError, ValidationError
from src.routes.meta_routes import router as metaroutes
from src.routes.tasks_routes import router as taskroutes
from src.repositories.tasks_repository import close_connection


@asynccontextmanager
async def lifespan(app:FastAPI):

    yield

    close_connection()



app = FastAPI(lifespan=lifespan)


app.include_router(metaroutes)
app.include_router(taskroutes)

app.add_exception_handler(NotFoundError, not_found_error)
app.add_exception_handler(ValidationError, validation_error)


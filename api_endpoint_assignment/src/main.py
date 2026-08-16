#Imports libraries and functions from different files
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.middleware.error_handler import validation_error, not_found_error, invalid_login
from src.errors import NotFoundError, ValidationError, InvalidCredentials
from src.routes.meta_routes import router as metaroutes
from src.routes.tasks_routes import router as taskroutes
from src.routes.auth_routes import router as authroutes
from src.repositories.tasks_repository import close_connection
from src.core.supabase_client import get_supabase



#Closes database and cursor when server stops
@asynccontextmanager
async def lifespan(app:FastAPI):

    supabase_client = get_supabase() #Get the supabase object
 
    app.state.supabase = supabase_client #Attach supabase to app's object

    yield

    close_connection() #Close con and cur


#Creats app object
app = FastAPI(lifespan=lifespan)


#connects router to app
app.include_router(metaroutes)
app.include_router(taskroutes)
app.include_router(authroutes)

#connects error classes to error handler functions
app.add_exception_handler(NotFoundError, not_found_error)
app.add_exception_handler(ValidationError, validation_error)
app.add_exception_handler(InvalidCredentials, invalid_login)
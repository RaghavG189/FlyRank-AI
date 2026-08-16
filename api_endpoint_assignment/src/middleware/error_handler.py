from src.errors import NotFoundError, ValidationError, InvalidCredentials
from fastapi.responses import JSONResponse

#Validaion error handler function that that takes message from class and returns to user
def validation_error(request, exc:ValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.message})

#Not found error handler function that takes message from class and returns to user
def not_found_error(request, exc:NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})

#Invalid login error handler function that take message from class and returns to user
def invalid_login(request, exc:InvalidCredentials):
    return JSONResponse(status_code=401, content={"detail": exc.message})

    
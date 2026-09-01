from src.errors import NotFoundError, ValidationError, InvalidCredentials, LLMQuarantineError, LLMDisabled
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

#Validaion error handler function that that takes message from class and returns to user
def validation_error(request, exc:ValidationError):
    return JSONResponse(status_code=400, content={"error": exc.message})

#Not found error handler function that takes message from class and returns to user
def not_found_error(request, exc:NotFoundError):
    return JSONResponse(status_code=404, content={"error": exc.message})

#Invalid login error handler function that take message from class and returns to user
def invalid_login(request, exc:InvalidCredentials):
    return JSONResponse(status_code=401, content={"error": exc.message})

#Request validation error function that returns field with error when fastapi raises RequestValidationError
def request_validation_error(request, exc:RequestValidationError):
    first_error = exc.errors()[0]
    field = first_error["loc"][-1]

    return JSONResponse(status_code=400, content={"error": f"{field}: {first_error['msg']}"})

#llm quarantine error function that returns field with error when fastapi raises llm quarantine error
def llm_quarantine_error(request, exc:LLMQuarantineError):
    return JSONResponse(status_code=422, content={"error": exc.message})

#llm_disabled function that returns message with error when fastapi raises llm_disabled
def llm_disabled(request, exc:LLMDisabled):
    return JSONResponse(status_code=503, content={"error": exc.message})
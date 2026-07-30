from src.errors import NotFoundError, ValidationError
from fastapi.responses import JSONResponse


def validation_error(request, exc:ValidationError):
    return JSONResponse(status_code=400, content={"detail": exc.message})

def not_found_error(request, exc:NotFoundError):
    return JSONResponse(status_code=404, content={"detail": exc.message})



    
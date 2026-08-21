from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.errors import InvalidCredentials
import src.repositories.auth_respository as a_repo



bearer_scheme = HTTPBearer(auto_error=False) #Creates HTTPBearer Scheme to be used for protected routes


def check_token(request:Request, credentials:HTTPAuthorizationCredentials | None = Depends(bearer_scheme)):

    #Checks if header is malformed or missing
    if credentials is None:

        raise InvalidCredentials("Access token required.") 

    #Gets token to be used for verifying user
    token = credentials.credentials

    response = a_repo.verify_token(token, request)

    return response


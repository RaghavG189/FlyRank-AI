from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime
import src.services.auth_services as auth


router = APIRouter(tags=['Auth'])


class Signup(BaseModel):
    email: str
    password: str

class SignupResponse(BaseModel):
    user_id: str
    email: str

@router.post("/auth/signup", status_code=201)
def sign_up(request:Request, signup:Signup):
    
    response = auth.sign_up_verify(signup.email, signup.password, request)
    
    return SignupResponse(user_id=response.id, email=response.email)


class Login(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

@router.post("/auth/login")
def login(request:Request, login:Login):

    response = auth.login_verify(login.email, login.password, request)

    return LoginResponse(access_token=response.access_token, refresh_token=response.refresh_token)


class CheckTokenResponse(BaseModel):
    id: str
    email: str
    account_date: datetime

bearer_scheme = HTTPBearer(auto_error=False)

@router.get("/protected/profile", status_code=200)
def protected_profile(request:Request, credentials:HTTPAuthorizationCredentials | None=Depends(bearer_scheme),):

    response = auth.check_token(request, credentials)

    return CheckTokenResponse(id=response.user.id, email=response.user.email, account_date=response.user.created_at)
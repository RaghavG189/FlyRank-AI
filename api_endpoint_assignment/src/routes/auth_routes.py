from fastapi import APIRouter, Request
from pydantic import BaseModel
import src.services.auth_services as auth


router = APIRouter()


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

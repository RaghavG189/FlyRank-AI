from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
from datetime import datetime
import src.services.auth_services as auth
import src.middleware.verification as verify


router = APIRouter(tags=['Auth'])


class Signup(BaseModel): #Pydantic model to enforce email and password
    email: str
    password: str

class SignupResponse(BaseModel): #Pydantic model to return userid & email from JSON body
    user_id: str
    email: str

@router.post("/auth/signup", status_code=201) #Endpoint that lets user signup with email & password
def sign_up(request:Request, signup:Signup):
    
    response = auth.sign_up_verify(signup.email, signup.password, request)
    
    return SignupResponse(user_id=response.id, email=response.email)


class Login(BaseModel): #Pydantic model to enforce email and password
    email: str
    password: str

class LoginResponse(BaseModel): #Pydantic model to return access token and refresh token
    access_token: str
    refresh_token: str

@router.post("/auth/login") #Endpoint that lets user login with email and password
def login(request:Request, login:Login):

    response = auth.login_verify(login.email, login.password, request)

    return LoginResponse(access_token=response.access_token, refresh_token=response.refresh_token)


class CheckTokenResponse(BaseModel): #Pydantic model to return id, email, & account date. No model for enforcing variables
    id: str
    email: str
    account_date: datetime

@router.get("/protected/profile", status_code=200) #Gives user metadata given valid token
def protected_profile(current_user=Depends(verify.check_token)): #First checks if token is valid

    return CheckTokenResponse(id=current_user.id, email=current_user.email, account_date=current_user.created_at)


@router.post("/auth/logout", status_code=204) #Logs user out of all current sessions
def logout(request:Request, current_user=Depends(verify.check_token)): #First checks if token is valid

    auth.logout_verify(request)
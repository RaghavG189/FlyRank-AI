import src.repositories.auth_respository as a_repo
from src.errors import NotFoundError, ValidationError, InvalidCredentials


#Business logic for signup endpoint that makes sure email and password are provided/valid
def sign_up_verify(email:str, password:str, request):

    if email is None or password is None:

        raise ValidationError("You must provide both email and password.")

    if email.strip() == "":

        raise ValidationError("Email cannot be empty.")
        
    if password.strip() == "":

        raise ValidationError("Password cannot be empty.")

    response = a_repo.sign_up_auth(email, password, request)

    return response   


#Function that verifies email and password are provided/valid for login
def login_verify(email:str, password:str, request):

    if email is None or password is None:

        raise ValidationError("You must provide both email and password.")

    if email.strip() == "":

        raise ValidationError("Email cannot be empty.")
        
    if password.strip() == "":

        raise ValidationError("Password cannot be empty.")

    response = a_repo.login_auth(email, password, request)

    return response


#Function that passes request to function in auth_repository for logout. No business logic needed.
def logout_verify(request):

    return a_repo.logout_auth(request)
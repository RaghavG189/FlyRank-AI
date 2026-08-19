import src.repositories.auth_respository as a_repo
from src.errors import NotFoundError, ValidationError, InvalidCredentials

def sign_up_verify(email:str, password:str, request):

    if email is None or password is None:

        raise ValidationError("You must provide both email and password.")

    if email.strip() == "":

        raise ValidationError("Email cannot be empty.")
        
    if password.strip() == "":

        raise ValidationError("Password cannot be empty.")

    response = a_repo.sign_up_auth(email, password, request)

    return response   


def login_verify(email:str, password:str, request):

    if email is None or password is None:

        raise ValidationError("You must provide both email and password.")

    if email.strip() == "":

        raise ValidationError("Email cannot be empty.")
        
    if password.strip() == "":

        raise ValidationError("Password cannot be empty.")

    response = a_repo.login_auth(email, password, request)

    return response


def check_token(request, credentials):
    #Checks if header is malformed or missing

    if credentials is None:

        raise InvalidCredentials("Access token required.") 

    token = credentials.credentials

    response = a_repo.verify_token(token, request)

    return response

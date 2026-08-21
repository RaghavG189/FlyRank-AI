from supabase_auth.errors import AuthApiError
from src.errors import InvalidCredentials

#Function that calls supabase and creates user account given email & password
def sign_up_auth(email, password, request):

    supabase = request.app.state.supabase #Retrieve client from app object

    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )

    return response.user


#Function that calls supabase and logs user in given email & password
def login_auth(email, password, request):

    supabase = request.app.state.supabase

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )

        return response.session

    except AuthApiError: #If login information is incorrect then raises InvalidCredentials error since "return response.session" wont happen
        raise InvalidCredentials("Invalid Login Credentials")
    

#Function that calls supabase to verify user token
def verify_token(token, request):

    supabase = request.app.state.supabase

    #Raise error if token invalid, expired, etc.
    try:
        response = supabase.auth.get_user(token)

        return response.user
    
    except AuthApiError: #If token is invalid then raises InvalidCredentials
        raise InvalidCredentials("Invalid or expired token")


#Calls supabase to log user out of session
def logout_auth(request):

    supabase = request.app.state.supabase

    supabase.auth.sign_out()



    
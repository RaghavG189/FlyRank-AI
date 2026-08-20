from supabase_auth.errors import AuthApiError
from src.errors import InvalidCredentials

def sign_up_auth(email, password, request):

    supabase = request.app.state.supabase

    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )

    return response.user


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

    except AuthApiError:
        raise InvalidCredentials("Invalid Login Credentials")
    

def verify_token(token, request):

    supabase = request.app.state.supabase

    #Raise error if token invalid, expired, etc.
    try:
        response = supabase.auth.get_user(token)

        return response.user
    
    except AuthApiError:
        raise InvalidCredentials("Invalid or expired token")


def logout_auth(request):

    supabase = request.app.state.supabase

    supabase.auth.sign_out()

    
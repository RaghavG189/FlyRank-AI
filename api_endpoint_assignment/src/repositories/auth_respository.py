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
    


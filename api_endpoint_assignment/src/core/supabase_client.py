import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

#Get url and key to create supabase object
url: str = os.environ["SUPABASE_URL"]
key: str = os.environ["SUPABASE_KEY"]

supabase: Client = create_client(url, key)


#Return supabase
def get_supabase():

    return supabase
from dotenv import load_dotenv
import os
from src.llm.schema import OutputValidation, Category, Experience
from openai import OpenAI

load_dotenv()


def call_client(text: str):

    if os.environ.get("LLM_STUB") == "1":

        return OutputValidation(
            category = Category.SWE,
            experience = Experience.INTERN,
            category_confidence = 0.9,
            experience_confidence = 0.8,
            reason = "This is a response from stubby."
        )
    '''
    else:

        client = OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])

        res = client.chat.completions.create(
            model=os.environ["LLM_MODEL"],
            messages=[{
                
            }]
        )

        return
    '''
from dotenv import load_dotenv
import os
from src.llm.schema import OutputValidation, Category, Experience
from openai import OpenAI
import json

load_dotenv()

def get_prompt():

    with open("prompts/your-job-v1.md", "r", encoding="utf-8") as f:

        system_prompt = f.read()

    return system_prompt


def call_client(text: str):

    if os.environ.get("LLM_STUB") == "1":

        return OutputValidation(
            category = Category.SWE,
            experience = Experience.INTERN,
            category_confidence = 0.9,
            experience_confidence = 0.8,
            reason = "This is a response from stubby."
        )
    
    else:

        client = OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"])


        system_prompt = get_prompt()

        res = client.chat.completions.create(
            model=os.environ["LLM_MODEL"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps({"job description": text})}
                ],
            temperature=0.0
        )

        return res.choices[0].message.content
    
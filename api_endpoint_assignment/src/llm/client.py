from dotenv import load_dotenv
import os
from openai import OpenAI
import json
from pydantic import ValidationError
from src.llm.schema import OutputValidation, Category, Experience
from src.llm.parse_repair import parse_repair_output
from src.errors import LLMQuarantineError

load_dotenv()


def get_prompt():

    with open("prompts/your-job-v1.md", "r", encoding="utf-8") as f:

        system_prompt = f.read()

    return system_prompt

def get_output(llm_response):

    #Call parse_repair function for LLM output
    response = parse_repair_output(llm_response)

    if response == None:

        raise ValueError("Your response failed to be parsed into JSON. Make sure you only return the JSON object excluding unnecessary text.")

    
    output = OutputValidation(
        category=response.get("category"), experience=response.get("experience"),
        category_confidence=response.get("category_confidence"), experience_confidence=response.get("experience_confidence"),
        reason=response.get("reason")
    )
    
    return output


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
        
        try:
            system_prompt = get_prompt()
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps({"job description": text})}
            ]

            res = client.chat.completions.create(
                    model=os.environ["LLM_MODEL"],
                    messages=messages,
                    temperature=0.0
                )
        
            llm_response = res.choices[0].message.content

            output = get_output(llm_response)
            return output
        
        except (ValidationError, ValueError) as e:

            try:
                #same prompt + broken llm output + exact validation error + "Your previous answer was rejected for this reason. Return only corrected JSON matching the schema."
                system_prompt = get_prompt()
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps({"job description": text})},
                    {"role": "assistant", "content": llm_response},
                    {"role": "user", "content": f"Your previous answer was rejected for this reason: {e}. Return only corrected JSON matching the schema."}
                ]            

                res = client.chat.completions.create(
                        model=os.environ["LLM_MODEL"],
                        messages=messages,
                        temperature=0.0
                    )
            
                llm_response = res.choices[0].message.content            

                output = get_output(llm_response)
                return output
            except (ValidationError, ValueError) as e:

                log = {
                    "user_input": text,
                    "llm_output": llm_response,
                    "error": str(e),
                    "prompt_version": "your-job-v1.md"
                }

                with open("src/logs/quarantine.jsonl", "a", encoding="utf-8") as f:
                    json.dump(log, f, indent=2)
                    f.write("\n")
                    
                
                raise LLMQuarantineError(str(e))

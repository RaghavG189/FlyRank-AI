from dotenv import load_dotenv
import os
from openai import OpenAI
import json
import time
from pydantic import ValidationError
from src.llm.schema import OutputValidation, Category, Experience
from src.llm.parse_repair import parse_repair_output
from src.errors import LLMQuarantineError, LLMDisabled

#Load .env variables
load_dotenv()


#Logs metadata on a failed/invalid LLM output
def log_bad_output(record:dict):

    with open("src/quarantine_logs/quarantine.jsonl", "a", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
        f.write("\n")

#Logs call data from the LLM 
def log_call_cost(record:dict):

    with open("src/call_logs/call.jsonl", "a", encoding="utf-8") as f:
        json.dump(record, f, indent=2)
        f.write("\n")



#Return system prompt to be used in LLM call
def get_prompt():

    with open("prompts/your-job-v1.md", "r", encoding="utf-8") as f:

        system_prompt = f.read()

    return system_prompt

#Returns validated LLM output
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



#Calls either predefined data or LLM to get output
def call_client(text: str):

    if os.environ.get("LLM_ENABLED") == "FALSE":

        raise LLMDisabled("The LLM has been turned off.")

    elif os.environ.get("LLM_STUB") == "1":

        return OutputValidation(
            category = Category.SWE,
            experience = Experience.INTERN,
            category_confidence = 0.9,
            experience_confidence = 0.8,
            reason = "This is a response from stubby."
        )
    
    else:

        #Create client object with timeout and retries
        client = OpenAI(base_url=os.environ["LLM_BASE_URL"], api_key=os.environ["LLM_API_KEY"], timeout=30.0, max_retries=2)
        
        try:
            system_prompt = get_prompt()

            #Passed into the LLM call with instructions and user input
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps({"job description": text})}
            ]

            start_time = time.perf_counter() #Track llm response time
            #LLM is called
            response = client.chat.completions.with_raw_response.create(
                model=os.environ["LLM_MODEL"],
                messages=messages,
                temperature=0.0 #0 for no variety
            )
            end_time = time.perf_counter() #Track llm response time

            res = response.parse()
            
            #Log the call data
            call_log = {
                "prompt_version": "your-job-v1.md",
                "model": res.model,
                "input_tokens": res.usage.prompt_tokens,
                "output_tokens": res.usage.completion_tokens,
                "duration": (end_time - start_time) / 1000,
                "repair": False 
            }
            log_call_cost(call_log)


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

                start_time = time.perf_counter()
                response = client.chat.completions.with_raw_response.create(
                        model=os.environ["LLM_MODEL"],
                        messages=messages,
                        temperature=0.0
                    )
                end_time = time.perf_counter()
                
                res = response.parse()
                
                #Log the call data
                call_log = {
                    "prompt_version": "your-job-v1.md",
                    "model": res.model,
                    "input_tokens": res.usage.prompt_tokens,
                    "output_tokens": res.usage.completion_tokens,
                    "duration": (end_time - start_time) / 1000,
                    "repair": True
                }
                log_call_cost(call_log)


            
                llm_response = res.choices[0].message.content            

                output = get_output(llm_response)
                return output
            except (ValidationError, ValueError) as e:

                #If llm output fails second time then log the details
                quarantine_log = {
                    "user_input": text,
                    "llm_output": llm_response,
                    "error": str(e),
                    "prompt_version": "your-job-v1.md"
                }

                log_bad_output(quarantine_log)
                    
                raise LLMQuarantineError(str(e))

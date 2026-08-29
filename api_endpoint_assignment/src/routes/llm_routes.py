#import libraries to create endpoint
from fastapi import FastAPI, Rou
from pydantic import BaseModel


router = FastAPI()


class InputValidation(BaseModel):

    input: str

class OutputValidation(BaseModel):

    category: str
    experience: str
    category_confidence: float
    experience_confidence: float
    reason: str


router.post("llm/job_classification")
def job_classification(inputvalidation:InputValidation):

    
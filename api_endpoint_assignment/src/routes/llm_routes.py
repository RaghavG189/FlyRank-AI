#import libraries to create endpoint
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Annotated
from src.llm.client import call_client

router = APIRouter(tags=['LLM'])





class InputValidation(BaseModel):

    input: Annotated[str, Field(min_length=1, max_length=6000)]

@router.post('/llm/job_classification')
def job_classification(inputvalidation:InputValidation):

    return call_client(inputvalidation.input)
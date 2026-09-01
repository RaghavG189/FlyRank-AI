from pydantic import BaseModel, Field
from typing import Annotated
from enum import Enum

#LLM needs to choose between these options
class Category(str, Enum): 
    SWE = "SWE"
    AI = "AI"
    DS = "DS"
    BACKEND = "Backend"
    FRONTEND = "Frontend"
    OTHER = "Other"

#LLM needs to choose between these options
class Experience(str, Enum):
    INTERN = "Intern"
    JUNIOR = "Junior"
    SENIOR = "Senior"
    OTHER = "Other"


#Schema the LLM needs to follow
class OutputValidation(BaseModel):

    category: Category
    experience: Experience
    category_confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    experience_confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    reason: str
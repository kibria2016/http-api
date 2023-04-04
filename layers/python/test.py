# from dataclasses import Field
# import pydantic
from pydantic import BaseModel, Field
from typing import List, Optional


class LoginTest(BaseModel):    
    email : str 
    password: str = Field(...,min_length=8)

# class AddTest(pydantic.BaseModel):
#     PK: Optional[str]
#     SK: Optional[str]
#     name : str

# class ListTest(pydantic.BaseModel):
#     tests : List[AddTest]
    
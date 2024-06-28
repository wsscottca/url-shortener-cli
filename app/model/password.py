''' Module contains password model for input validation '''

from pydantic import BaseModel, Field

class PasswordModel(BaseModel):
    ''' Password model for input validation '''
    password: str = Field(min_length=8, max_length=32)

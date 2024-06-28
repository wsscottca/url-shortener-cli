''' Module contains username model for input validation '''

from pydantic import BaseModel, Field

class UsernameModel(BaseModel):
    ''' Username model for input validation '''
    username: str = Field(min_length=4, max_length=16)

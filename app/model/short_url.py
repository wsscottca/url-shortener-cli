''' Module contains short url model for input validation '''

from pydantic import BaseModel, Field

class ShortUrlModel(BaseModel):
    ''' Short URL model for input validation '''
    short_url: str = Field(min_length=1, max_length=8)
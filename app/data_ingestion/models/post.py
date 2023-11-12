from pydantic import BaseModel

class Post(BaseModel):
    """Post is used to store content and publications from the front end"""
    content: str
    publication: str

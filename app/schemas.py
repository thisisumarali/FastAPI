from pydantic import BaseModel


class PostBase(BaseModel):
    name: str
    branch: str
    published: bool = True


class PostCreate(PostBase):
    pass

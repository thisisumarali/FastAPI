from fastapi import FastAPI, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    name: str
    branch: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/')
def home():
    return {"hello": "World"}


my_post = [
    {"id": 1, "name": "BNC",   "branch": "DEFENCE",
        "published": True,    "rating": 5},
    {"id": 2, "name": "BidecSol",   "branch": "Nursery",
        "published": False,    "rating": 4.5}
]
# CRUD


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p

# POST


@app.post('/posts')
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 999)
    my_post.append(post_dict)
    return {"Data": post_dict}

# GET ALL POSTS


@app.get('/posts')
def get_posts():
    return {"Data": my_post}


@app.get('/posts/latest')
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {'detail': post}
# GET BY ID


@app.get('/posts/{id}')
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found.")
    return {"Post": post}


# EDIT POST BY ID
@app.put('/posts/{id}')
def update_post():
    return {"Data": "World"}


# DELETE POST
@app.delete('/posts/{id}')
def delete_post():
    return {"Data": "World"}

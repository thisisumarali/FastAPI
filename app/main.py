from fastapi import FastAPI, status, HTTPException, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()


class Post(BaseModel):
    name: str
    branch: str
    published: bool = True


while True:

    try:
        conn = psycopg2.connect(host="localhost", database='fastapi',
                                user='postgres', password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successfull")
        break
    except Exception as error:
        print("connecting to db failed")
        print("Error: ", error)
        time.sleep(2)


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


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p['id'] == id:
            return i
# POST


# @app.post('/posts', status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     post_dict = post.model_dump()
#     post_dict['id'] = randrange(0, 999)
#     my_post.append(post_dict)
#     return {"Data": post_dict}

@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (name, branch, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.name, post.branch, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"Data": new_post}

# GET ALL POSTS


@app.get('/posts')
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    post = cursor.fetchall()
    return {"Data": post}


@app.get('/posts/latest')
def get_latest_post():
    post = my_post[len(my_post)-1]
    return {'detail': post}
# GET BY ID


@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found.")
    return {"Post": post}


# DELETE POST
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    delete_post = cursor.fetchone()
    conn.commit()
    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found.")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# EDIT POST BY ID
@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET name = %s, branch = %s, published = %s WHERE id = %s RETURNING * """, (post.name, post.branch, post.published, str(id)))
    update_post = cursor.fetchone()
    conn.commit()
    if update_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found.")

    return {"data": update_post}

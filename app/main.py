from random import randrange
from typing import Optional
from fastapi import FastAPI , Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

#***************************************************************

app = FastAPI()


try:
    conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='2001',
                            cursor_factory=RealDictCursor)
    cur = conn.cursor()
    cur.execute('SELECT version()')
    db_version = cur.fetchone()
    print(db_version)
    print('PostgreSQL database connection established.')
except (Exception, psycopg2.DatabaseError) as error:
    print(error)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True



#***************************************************************

@app.get("/")
async def root():
    return {"message": "Hello World"}

#***************************************************************

@app.get("/posts")
async def get_posts():
    cur.execute("SELECT * FROM post")
    posts = cur.fetchall()
    print(posts)
    return {"data": posts}

#***************************************************************

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    cur.execute("SELECT * FROM post WHERE id= %s ", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Post with id {id} not found"}
    return {"data": post}

#***************************************************************

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def creat_post(post: Post):
    cur.execute("INSERT INTO post (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
                (post.title, post.content, post.published))
    post = cur.fetchone()
    conn.commit()
    return {"data": post}

#***************************************************************

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cur.execute("DELETE FROM post WHERE id= %s RETURNING *", (str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#***************************************************************

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cur.execute("UPDATE post SET title = %s, content = %s, published = %s WHERE id= %s RETURNING *",
                (post.title,post.content,post.published,str(id),))
    post = cur.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id {id} not found",
            )
    conn.commit()
    return {"data": post}

#***************************************************************
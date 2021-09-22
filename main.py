import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Blog(BaseModel):
    id: int
    title: str
    body: str


@app.get('/')
def index():
    return {"data": {"name": "Sanjar"}}


@app.get('/about')
def about():
    return {"data": "about page"}


@app.post('/blog')
def create_blog(blog: Blog):
    return {"data": f"Blog is created {blog.title}"}


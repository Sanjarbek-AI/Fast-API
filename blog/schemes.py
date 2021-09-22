from typing import List

from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


class ShowBlog(BaseModel):
    id: int
    title: str
    body: str

    class Config:
        orm_mode = True


class User(BaseModel):
    name: str
    email: str
    password: str


class ShowUser(BaseModel):
    id: int
    name: str
    email: str

    blogs: List

    class Config:
        orm_mode = True

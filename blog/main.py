from typing import List

from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from . import schemes, models
from .database import engine, get_db
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_blog(request: schemes.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog:
        HTTPException(status_code=404, detail=f"Blog with this id {blog_id} is not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog is deleted)"}


@app.put('/blog/{blog_id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update_blog(blog_id, request: schemes.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with this id ({blog_id}) is not found")

    blog.update({'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return {"detail": "Blog is updated"}


@app.get('/blog', response_model=List[schemes.ShowBlog], tags=["Blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@app.get('/blog/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemes.ShowBlog, tags=["Blogs"])
def get_one_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with this id {blog_id} is not found")
    return blog


@app.post('/user', status_code=status.HTTP_201_CREATED, response_model=schemes.ShowUser, tags=["Users"])
def create_user(request: schemes.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/user', response_model=List[schemes.ShowUser], tags=["Users"])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


@app.get('/user/{user_id}', tags=["Users"])
def get_one_user(user_id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with this id ({user_id}) is not found")
    return user

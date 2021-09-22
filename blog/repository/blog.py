from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemes
from ..database import get_db


def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


def create_blog(request: schemes.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog:
        HTTPException(status_code=404, detail=f"Blog with this id {blog_id} is not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog is deleted)"}


def update_blog(blog_id, request: schemes.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with this id ({blog_id}) is not found")

    blog.update({'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return {"detail": "Blog is updated"}


def get_one_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with this id {blog_id} is not found")
    return blog
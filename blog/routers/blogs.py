from typing import List

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemes, models
from ..database import get_db

router = APIRouter(
    tags=["Blogs"],
    prefix="/blog"
)


@router.get('/', response_model=List[schemes.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    return db.query(models.Blog).all()


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemes.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)

    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog:
        HTTPException(status_code=404, detail=f"Blog with this id {blog_id} is not found")

    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": "Blog is deleted)"}


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id, request: schemes.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=404, detail=f"Blog with this id ({blog_id}) is not found")

    blog.update({'title': request.title, 'body': request.body}, synchronize_session=False)
    db.commit()
    return {"detail": "Blog is updated"}


@router.get('/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemes.ShowBlog)
def get_one_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail=f"Blog with this id {blog_id} is not found")
    return blog

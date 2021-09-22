from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemes
from ..database import get_db
from ..repository import blog

router = APIRouter(
    tags=["Blogs"],
    prefix="/blog"
)


@router.get('/', response_model=List[schemes.ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    return blog.get_all_blogs(db)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemes.Blog, db: Session = Depends(get_db)):
    return blog.create_blog(request, db)


@router.delete('/{blog_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id, db: Session = Depends(get_db)):
    return blog.delete_blog(blog_id, db)


@router.put('/{blog_id}', status_code=status.HTTP_202_ACCEPTED)
def update_blog(blog_id, request: schemes.Blog, db: Session = Depends(get_db)):
    return blog.update_blog(blog_id, request, db)


@router.get('/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemes.ShowBlog)
def get_one_blog(blog_id, db: Session = Depends(get_db)):
    return blog.get_one_blog(blog_id, db)

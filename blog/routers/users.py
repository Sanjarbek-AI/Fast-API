from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .. import schemes
from ..database import get_db
from ..repository import user

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)


@router.get('/', response_model=List[schemes.ShowUser])
def get_all_users(db: Session = Depends(get_db)):
    return user.get_all_users(db)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemes.ShowUser)
def create_user(request: schemes.User, db: Session = Depends(get_db)):
    return user.create_user(request, db)


@router.get('/{user_id}')
def get_one_user(user_id, db: Session = Depends(get_db)):
    return user.get_one_user(user_id, db)


@router.put('/user', response_model=schemes.ShowUser)
def update_user(user_id, request: schemes.User, db: Session = Depends(get_db)):
    return user.update_user(user_id, request, db)

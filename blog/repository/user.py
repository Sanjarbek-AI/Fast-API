from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemes, models
from ..database import get_db
from ..hashing import Hash


def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


def create_user(request: schemes.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_one_user(user_id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"User with this id ({user_id}) is not found")
    return user

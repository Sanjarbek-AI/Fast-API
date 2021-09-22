from sqlalchemy import Column, Integer, String
from .database import Base


class Blog(Base):
    __tablename__ = "Blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)

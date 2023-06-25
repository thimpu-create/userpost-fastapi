from .database import Base
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship,mapped_column

class User(Base):
    __tablename__ = 'user'
    id = mapped_column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,unique=True)
    password = Column(String)
    post = relationship("Post",back_populates="owner",cascade="all, delete,delete-orphan",passive_deletes=True)

class Post(Base):
    __tablename__ = 'post'
    id = mapped_column(Integer,primary_key=True,autoincrement=True)
    owner_id = mapped_column(Integer,ForeignKey('user.id',ondelete="CASCADE"))
    title = Column(String)
    owner = relationship("User",back_populates="post")
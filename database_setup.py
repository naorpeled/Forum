import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    photoURL = Column(String)
    bio = Column(String)


class Categories(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories)
    author_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)
    time = Column(DateTime, default=func.now())

class Comments(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users)
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Posts)
    time = Column(DateTime, default=func.now())

engine = create_engine('sqlite:///forum_database.db')


Base.metadata.create_all(engine)
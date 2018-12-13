import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    """
    Registered user information is stored in db
    """
    __tablename__ = 'users'

    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=True)
    photoURL = Column(String)
    bio = Column(String)
    rank = Column(Integer)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'password': self.password,
            'photoURL': self.photoURL,
            'rank': self.rank,
        }


class Categories(Base):
    """
    Store categories info in db
    """
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class Posts(Base):
    """
    Store posts info in db.

    Stores the post's title, content, category id
    author, time of creation.
    """
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    content = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship(Categories, cascade="all, delete-orphan")
    author_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users, cascade="all, delete-orphan")
    time = Column(DateTime, default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category_id': self.category_id,
            'author_id': self.author_id,
            'time': self.time,
        }


class Comments(Base):
    """
    Stores comment information in the db

    Stores the comment content, author,
    to which post is it connected to.
    """
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    author_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(Users, cascade="all, delete-orphan")
    post_id = Column(Integer, ForeignKey('posts.id'))
    post = relationship(Posts, cascade="all, delete-orphan")
    time = Column(DateTime, default=func.now())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'content': self.content,
            'post_id': self.post_id,
            'author_id': self.author_id,
            'time': self.time,
        }


engine = create_engine('sqlite:///forum_database.db')


Base.metadata.create_all(engine)

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime
from sqlalchemy.sql import func
from passlib.apps import custom_app_context as pwd_context
import random
import string
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
        }


class User(Base):
    __tablename__ = 'user'
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)


class Item(Base):
    __tablename__ = 'item'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    time_added = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category_name = Column(String(80), ForeignKey('category.name'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'user_id': self.user_id,
            'category_name': self.category_name,
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)

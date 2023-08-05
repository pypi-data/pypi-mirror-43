from sqlalchemy import (Column, DateTime, Integer, String, Unicode,
                        UnicodeText, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .msg import Message
from .utils import get_engine


class User(declarative_base(bind=get_engine())):
    __tablename__ = 'users'

    username = Column(String(), nullable=False, index=True)
    password = Column(String(), nullable=False)
    messages = relationship('Message', backref='user')

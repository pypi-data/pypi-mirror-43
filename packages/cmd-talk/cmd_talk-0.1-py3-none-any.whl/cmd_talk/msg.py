from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Unicode,
                        UnicodeText, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from tzlocal import get_localzone

from .utils import get_engine


class Message(declarative_base(bind=get_engine())):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(UnicodeText(), nullable=False)
    time = Column(DateTime(), nullable=False)

    def __init__(self, *args, **kwargs):
        self.id = Message.id
        Message.id += 1

        if 'content' in kwargs.keys():
            self.content = kwargs['content']
        else:
            raise Exception('No content in message, id=%d' % (self.id))

        if 'time' in kwargs.keys():
            self.time = kwargs['time']
        else:
            self.time = datetime.now(tzinfo=get_localzone())

    def __eq__(self, value):
        return (
            self.id == value.id and
            self.content == value.content and
            self.time == value.time
        )

    def __str__(self):
        return 'Message: content="%s", time="%s", id="%d".' % (
            self.content, self.time, self.id
        )

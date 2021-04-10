from os import path
from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, TIMESTAMP, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship, backref

from src.db.helpers import GUID

db_path = path.join(path.dirname(__file__), 'kursachgram.db')
engine = create_engine(f'sqlite:///{db_path}')
base = declarative_base()


class User(base):
    __tablename__ = 'users'

    id = Column(GUID(), primary_key=True, default=uuid4)
    email = Column(String(100), unique=True)
    avatar_base64 = Column(Text)
    username = Column(String(100))
    online = Column(Boolean)
    sid = Column(String(100))
    logout_timestamp = Column(TIMESTAMP, default=datetime.utcnow)
    password = Column(Text)

    def jsonify(self):
        # ONLY NON PRIVATE DATA CAN BE SHARED
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'avatar_base64': self.avatar_base64,
            'online': self.online,
            'logout_timestamp': self.logout_timestamp.timestamp()
        }

    def __repr__(self):
        return f'<User(email={self.email}, ' \
               f'username={self.username}, ' \
               f'avatar_base64={not (self.avatar_base64 is None)}), ' \
               f'online={self.online}, ' \
               f'sid={self.sid}, ' \
               f'logout_timestamp={self.logout_timestamp}>'


chat_participants = Table(
    'chat_participants',
    base.metadata,
    Column('user_id', GUID(), ForeignKey('users.id'), primary_key=True),
    Column('chat_id', GUID(), ForeignKey('chats.id'), primary_key=True),
)


class Chat(base):
    __tablename__ = 'chats'

    id = Column(GUID(), primary_key=True, default=uuid4)
    name = Column(Text, nullable=True)
    avatar_base64 = Column(Text, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", backref="created_chats")
    participants = relationship("User", secondary=chat_participants, lazy='subquery', backref=backref('chats', lazy=True))

    def jsonify(self):
        # ONLY NON PRIVATE DATA CAN BE SHARED
        return {
            'id': self.id,
            'name': self.name,
            'avatar_base64': self.avatar_base64,
            'creator_id': self.creator_id,
            'participants_ids': list(map(lambda p: p.id, self.participants)),
        }

    def __repr__(self):
        return f'<Chat(id={self.id}, ' \
               f'name={self.name}, ' \
               f'avatar_base64={not (self.avatar_base64 is None)}), ' \
               f'creator_id={self.creator_id}, ' \
               f'participants={len(self.participants)}>'


base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

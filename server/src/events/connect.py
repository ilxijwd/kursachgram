import os

import jwt

from src.db import session, User
from src.responses import users, user_online, error
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: connect')

    @sio.event
    def connect(sid, environ, auth=None):
        print('[sio] emitted: connect')

        if not auth or 'token' not in auth:
            return

        try:
            jwt_payload = jwt.decode(auth['token'], os.environ.get("JWT_SECRET"), algorithms=['HS256'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return error(sio, sid, Errors.INVALID_AUTHENTICATION_TOKEN)

        user = session.query(User).filter(User.email == jwt_payload['email']).first()
        if not user:
            return error(sio, sid, Errors.NOT_AUTHENTICATED)

        user.online = True
        user.sid = sid
        session.commit()

        sio.save_session(sid, user.jsonify())

        registered_users = session.query(User).filter(User.id != user.id).all()
        users(sio, sid, registered_users)

        for chat in user.chats:
            sio.enter_room(user.sid, chat.id)

        user_online(sio, sid, user.id)

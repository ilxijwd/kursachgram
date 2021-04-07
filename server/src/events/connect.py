import os

import jwt

from src.db import session, User, Chat
from src.responses import invalid_token, not_registered, users, user_online


def register_event(sio):
    print('[sio] event registered: connect')

    @sio.event
    def connect(sid, environ, auth=None):
        # if not authenticated
        if not auth or 'token' not in auth:
            return

        try:
            jwt_payload = jwt.decode(auth['token'], os.environ.get("JWT_SECRET"), algorithms=['HS256'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return invalid_token(sio, sid)

        user = session.query(User).filter(User.email == jwt_payload['email']).first()

        if not user:
            return not_registered(sio, sid)

        user.online = True
        user.sid = sid
        session.commit()

        sio.save_session(sid, user.jsonify())

        registered_users = session.query(User).filter(User.email != user.email).all()
        users(sio, sid, registered_users)

        for chat in user.chats:
            sio.enter_room(user.sid, chat.id)

        user_online(sio, sid, user.email)

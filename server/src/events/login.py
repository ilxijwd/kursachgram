import os
from datetime import datetime, timedelta

import jwt
from werkzeug.security import check_password_hash

from src.db import session, User
from src.responses import error, logged_in, users, user_online
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: login')

    @sio.event
    def login(sid, data):
        print('[sio] emitted: login')

        user_session = sio.get_session(sid)
        if user_session:
            return error(sio, sid, Errors.ALREADY_LOGGED_IN)

        if not data or 'email' not in data or 'password' not in data:
            return error(sio, sid, Errors.INVALID_REQUEST_DATA)

        user = session.query(User).filter(User.email == data['email']).first()
        if not user:
            return error(sio, sid, Errors.USER_BY_EMAIL_NOT_FOUND)

        if not check_password_hash(user.password, data['password']):
            return error(sio, sid, Errors.INVALID_PASSWORD)

        user.online = True
        user.sid = sid
        session.commit()

        payload = {
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 30)
        }

        logged_in(sio, sid, jwt.encode(payload, os.environ.get("JWT_SECRET"), algorithm='HS256'), user.jsonify())

        registered_users = session.query(User).filter(User.id != user.id).all()
        users(sio, sid, registered_users)

        for chat in user.chats:
            sio.enter_room(user.sid, chat.id)

        user_online(sio, sid, user.id)

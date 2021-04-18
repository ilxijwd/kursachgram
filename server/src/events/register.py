import os
from datetime import datetime, timedelta

import jwt
from werkzeug.security import generate_password_hash

from src.db import session, User
from src.responses import error, logged_in, user_online, users
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: register')

    @sio.event
    def register(sid, data):
        print('[sio] emitted: register')

        if not data or 'avatar_base64' not in data or 'username' not in data or 'email' not in data or 'password' not in data:
            return error(sio, sid, Errors.INVALID_REQUEST_DATA)

        user = session.query(User).filter(User.email == data['email']).first()
        if user:
            return error(sio, sid, Errors.EMAIL_ALREADY_IN_USE)

        new_user = User(
            email=data['email'],
            avatar_base64=data['avatar_base64'],
            username=data['username'],
            password=generate_password_hash(data['password']),
            online=True,
            sid=sid
        )

        session.add(new_user)
        session.commit()

        payload = {
            'id': new_user.id,
            'exp': datetime.now() + timedelta(seconds=60 * 60 * 24 * 30)
        }

        logged_in(sio, sid, jwt.encode(payload, os.environ.get("JWT_SECRET"), algorithm='HS256'), new_user)

        sio.save_session(sid, new_user.jsonify())

        user_online(sio, sid, new_user)

        online_users = session.query(User).filter(User.id != new_user.id).all()
        users(sio, sid, online_users)

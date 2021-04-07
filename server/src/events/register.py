import os
from datetime import datetime, timedelta

import jwt
from werkzeug.security import generate_password_hash

from src.db import session, User


def register_event(sio):
    print('[sio] event registered: register')

    @sio.event
    def register(sid, data):
        if not data or 'avatar_base64' not in data or 'username' not in data or 'email' not in data or 'password' not in data:
            return {'success': False, 'error': 'Invalid request data'}

        user = session.query(User).filter(User.email == data['email']).first()

        if user:
            return {'success': False, 'error': 'That email is already in use'}

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
            'email': new_user.email,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 30)
        }

        return {
            'success': True,
            'token': jwt.encode(payload, os.environ.get("JWT_SECRET"), algorithm='HS256'),
            'account_data': new_user.jsonify()
        }

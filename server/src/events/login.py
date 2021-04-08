import os
from datetime import datetime, timedelta

import jwt
from werkzeug.security import check_password_hash

from src.db import session, User


def register_event(sio):
    print('[sio] event registered: login')

    @sio.event
    def login(sid, data):
        print('[sio] emitted: login')

        if not data or 'email' not in data or 'password' not in data:
            return {'success': False, 'error': 'Invalid request data'}

        user = session.query(User).filter(User.email == data['email']).first()

        if not user:
            return {'success': False, 'error': 'User by this email was not found!'}

        if not check_password_hash(user.password, data['password']):
            return {'success': False, 'error': 'Invalid password'}

        user.online = True
        user.sid = sid
        session.commit()

        payload = {
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24 * 30)
        }

        return {
            'success': True,
            'token': jwt.encode(payload, os.environ.get("JWT_SECRET"), algorithm='HS256'),
            'account_data': user.jsonify()
        }

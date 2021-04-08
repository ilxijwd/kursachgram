import os

import jwt

from src.db import session, User, Chat
from src.responses import not_registered, invalid_token, message_sent


def register_event(sio):
    print('[sio] event registered: send_message')

    @sio.event
    def send_message(sid, data, auth=None):
        print('[sio] emitted: send_message')

        if not auth or 'token' not in auth:
            return

        if not data or 'sender_id' not in data or 'chat_id' not in data or 'content' not in data:
            return

        try:
            payload = jwt.decode(auth['token'], os.environ.get("JWT_SECRET"), algorithms=['HS256'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return invalid_token(sio, sid)

        user = session.query(User).filter(User.email == payload['email']).first()

        if not user:
            return not_registered(sio, sid)

        chat = session.query(Chat).filter(Chat.id == data['chat_id']).first()

        if not chat:
            return {'success': False, 'error': 'Chat was not found'}

        message_sent(sio, data['sender_id'], chat.id, data['content'], data.get('files'))

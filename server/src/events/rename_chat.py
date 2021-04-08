import os

import jwt

from src.db import session, User, Chat
from src.responses import not_registered, invalid_token, chat_renamed


def register_event(sio):
    print('[sio] event registered: rename_chat')

    @sio.event
    def rename_chat(sid, data, auth=None):
        print('[sio] emitted: rename_chat')

        if not auth or 'token' not in auth:
            return

        if not data or 'sender_id' not in data or 'chat_id' not in data or 'name' not in data:
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

        if chat.creator_id != user.id:
            return {'success': False, 'error': 'Chat is not owned by you'}

        chat.name = data['name']
        session.commit()

        chat_renamed(sio, chat.id, data['name'])
        return {'success': True}

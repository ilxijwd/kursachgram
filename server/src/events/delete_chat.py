import os

import jwt

from src.db import session, User, Chat
from src.responses import not_registered, invalid_token, chat_deleted


def register_event(sio):
    print('[sio] event registered: delete_chat')

    @sio.event
    def delete_chat(sid, data, auth=None):
        print('[sio] emitted: delete_chat')

        if not auth or 'token' not in auth:
            return

        if not data or 'sender_id' not in data or 'chat_id' not in data:
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

        session.delete(chat)
        session.commit()

        chat_deleted(sio, chat.id)
        return {'success': True}
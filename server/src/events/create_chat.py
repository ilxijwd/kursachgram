import os

import jwt

from src.db import session, User, Chat
from src.responses import not_registered, invalid_token, chat_created


def register_event(sio):
    print('[sio] event registered: create_chat')

    @sio.event
    def create_chat(sid, data, auth=None):
        if not auth or 'token' not in auth:
            return

        if not data or 'participants_ids' not in data:
            return

        try:
            payload = jwt.decode(auth['token'], os.environ.get("JWT_SECRET"), algorithms=['HS256'])
        except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidSignatureError):
            return invalid_token(sio, sid)

        user = session.query(User).filter(User.email == payload['email']).first()

        if not user:
            return not_registered(sio, sid)

        if user.id not in data['participants_ids']:
            return {'success': False, 'error': 'Creator must be in participants list too'}

        participants = session.query(User).filter(User.id.in_(data['participants_ids'])).all()
        if len(participants) < 2:
            return {'success': False, 'error': 'Not enough participants'}

        chat = Chat(
            name=data.get('name'),
            avatar_base64=data.get('avatar_base64'),
            creator=user,
            participants=participants
        )

        session.add(chat)
        session.commit()

        for participant_id in chat.jsonify()['participants_ids']:
            sio.enter_room(participant_id, chat.id)

        chat_created(sio, chat, chat.id)

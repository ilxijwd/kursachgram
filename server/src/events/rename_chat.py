from src.db import session, Chat
from src.responses import error, chat_renamed
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: rename_chat')

    @sio.event
    def rename_chat(sid, data):
        print('[sio] emitted: rename_chat')

        user_session = sio.get_session(sid)
        if not user_session:
            return error(sio, sid, Errors.NOT_AUTHENTICATED)

        if not data or 'chat_id' not in data or 'name' not in data:
            return error(sio, sid, Errors.INVALID_REQUEST_DATA)

        chat = session.query(Chat).filter(Chat.id == data['chat_id']).first()

        if not chat:
            return error(sio, sid, Errors.CHAT_WAS_NOT_FOUND)

        if chat.creator_id != user_session['id']:
            return error(sio, sid, Errors.INVALID_CHAT_OWNER)

        chat.name = data['name']
        session.commit()

        chat_renamed(sio, chat)

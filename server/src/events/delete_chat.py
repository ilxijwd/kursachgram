from src.db import session, Chat
from src.responses import error, chat_deleted
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: delete_chat')

    @sio.event
    def delete_chat(sid, data):
        print('[sio] emitted: delete_chat')

        user_session = sio.get_session(sid)
        if not user_session:
            return error(sio, sid, Errors.NOT_AUTHENTICATED)

        if not data or 'chat_id' not in data:
            return error(sio, sid, Errors.INVALID_REQUEST_DATA)

        chat = session.query(Chat).filter(Chat.id == data['chat_id']).first()

        if not chat:
            return error(sio, sid, Errors.CHAT_WAS_NOT_FOUND)

        if chat.creator_id != user_session['id']:
            return error(sio, sid, Errors.INVALID_CHAT_OWNER)

        session.delete(chat)
        session.commit()

        chat_deleted(sio, chat.id)

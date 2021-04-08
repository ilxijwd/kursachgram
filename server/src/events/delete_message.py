from src.db import session, Chat
from src.responses import error, message_deleted
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: delete_message')

    @sio.event
    def delete_message(sid, data):
        print('[sio] emitted: delete_message')

        user_session = sio.get_session(sid)
        if not user_session:
            return error(sio, sid, Errors.NOT_AUTHENTICATED)

        if not data or 'chat_id' not in data or 'msg_id' not in data:
            return error(sio, sid, Errors.INVALID_REQUEST_DATA)

        chat = session.query(Chat).filter(Chat.id == data['chat_id']).first()

        if not chat:
            return error(sio, sid, Errors.CHAT_WAS_NOT_FOUND)

        if chat.creator_id != user_session['id']:
            return error(sio, sid, Errors.INVALID_CHAT_OWNER)

        message_deleted(sio, chat.id, data['msg_id'])

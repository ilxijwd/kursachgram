from src.db import session, Chat
from src.responses import error, message_sent
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: send_message')

    @sio.event
    def send_message(sid, data):
        print('[sio] emitted: send_message')

        user_session = sio.get_session(sid)
        if not user_session:
            return error(sio, sid, Errors.NOT_AUTHENTICATED)

        if not data or 'chat_id' not in data or 'content' not in data:
            return error(sio, sid, Errors.INVALID_REQUEST_DATA)

        chat = session.query(Chat).filter(Chat.id == data['chat_id']).first()

        if not chat:
            return error(sio, sid, Errors.CHAT_WAS_NOT_FOUND)

        message_sent(sio, user_session['id'], chat.id, data['content'], data.get('files'))

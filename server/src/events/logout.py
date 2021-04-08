from src.db import session, User
from src.responses import error, user_offline
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: logout')

    @sio.event
    def logout(sid, data):
        print('[sio] emitted: logout')

        user_session = sio.get_session(sid)
        if not user_session:
            return

        user = session.query(User).filter(User.id == user_session['id']).first()
        if not user:
            return error(sio, sid, Errors.USER_BY_EMAIL_NOT_FOUND)  # TODO: CHANGE ERROR CODE TO "USER_NOT_FOUND"

        user.online = False
        session.commit()

        for chat in user.chats:
            sio.leave_room(user.sid, chat.id)

        user_offline(sio, sid, user.id)

        sio.save_session(sid, None)

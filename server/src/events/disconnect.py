from datetime import datetime

from src.db import session, User
from src.responses import user_offline, error
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: disconnect')

    @sio.event
    def disconnect(sid):
        print('[sio] emitted: disconnect')

        user_session = sio.get_session(sid)
        if not user_session or 'email' not in user_session:
            return

        user = session.query(User).filter(User.id == user_session['id']).first()
        if not user:
            return error(sio, sid, Errors.NOT_AUTHENTICATED)

        user.online = False
        user.logout_timestamp = datetime.utcnow()
        session.commit()

        user_offline(sio, sid, user)

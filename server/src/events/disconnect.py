from datetime import datetime

from src.db import session, User
from src.responses import not_registered, user_offline


def register_event(sio):
    print('[sio] event registered: disconnect')

    @sio.event
    def disconnect(sid):
        user_session = sio.get_session(sid)

        # sid has no login data
        if 'email' not in user_session:
            return

        user = session.query(User).filter(User.email == user_session['email']).first()

        if not user:
            return not_registered(sio, sid)

        user.online = False
        user.logout_timestamp = datetime.utcnow()
        session.commit()

        return user_offline(sio, sid, user.id)

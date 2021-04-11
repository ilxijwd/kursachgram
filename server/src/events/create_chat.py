from src.db import session, User, Chat
from src.responses import error, chat_created
from src.errors import Errors


def register_event(sio):
    print('[sio] event registered: create_chat')

    @sio.event
    def create_chat(sid, data):
        print('[sio] emitted: create_chat')

        user_session = sio.get_session(sid)
        if not user_session:
            return error(sio, sid, Errors.NOT_AUTHENTICATED)

        if not data or 'participants_ids' not in data:
            return error(sio, sid, Errors.INVALID_REQUEST_DATA)

        participants = session.query(User).filter(User.id.in_(data['participants_ids'])).all()
        user = session.query(User).filter(User.id == user_session['id']).first()
        participants.append(user)
        if len(participants) < 2:
            return error(sio, sid, Errors.NOT_ENOUGH_PARTICIPANTS)

        chat = Chat(
            name=data.get('name'),
            avatar_base64=data.get('avatar_base64'),
            creator=user,
            participants=participants
        )

        session.add(chat)
        session.commit()

        for participant in participants:
            sio.enter_room(participant.sid, chat.id)

        chat_created(sio, chat)

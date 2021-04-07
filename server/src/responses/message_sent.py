from uuid import uuid4


def message_sent(sio, sender_id, chat_id, content, files=None):
    sio.emit(
        'message_sent',
        {
            'id': str(uuid4()),
            'sender_id': sender_id,
            'сhat_id': chat_id,
            'content': content,
            'files': files or [],
        },
        room=chat_id,
    )

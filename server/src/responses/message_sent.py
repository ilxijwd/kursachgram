from uuid import uuid4


def message_sent(sio, sender, chat, content, files=None):
    chat_data = chat.jsonify()
    sio.emit(
        'message_sent',
        {
            'id': str(uuid4()),
            'sender': sender.jsonify(),
            'сhat': chat_data,
            'content': content,
            'files': files or [],
        },
        room=chat_data['id'],
    )

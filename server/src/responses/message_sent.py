from uuid import uuid4
from src.emojifier import emojifier


def message_sent(sio, sender, chat, content, files=None):
    chat_data = chat.jsonify()
    sio.emit(
        'message_sent',
        {
            'id': str(uuid4()),
            'sender': sender.jsonify(),
            'chat': chat_data,
            'content': emojifier(content) if content else '<empty message>',
            'files': files or [],
        },
        room=chat_data['id'],
    )

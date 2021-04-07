def chat_renamed(sio, chat_id, name):
    sio.emit('chat_renamed', {'id': chat_id, 'name': name}, room=chat_id)

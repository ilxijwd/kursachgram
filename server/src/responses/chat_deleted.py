def chat_deleted(sio, chat_id):
    sio.emit('chat_deleted', {'id': chat_id}, room=chat_id)

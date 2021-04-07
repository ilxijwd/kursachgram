def message_deleted(sio, chat_id, msg_id):
    sio.emit('message_deleted', {'chat_id': chat_id, 'msg_id': msg_id}, room=chat_id)

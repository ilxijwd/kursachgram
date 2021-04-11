def chat_deleted(sio, chat):
    chat_data = chat.jsonify()
    sio.emit('chat_deleted', chat_data, room=chat_data['id'])

def chat_created(sio, chat):
    chat_data = chat.jsonify()
    sio.emit('chat_created', chat_data, room=chat_data['id'])

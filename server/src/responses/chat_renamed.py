def chat_renamed(sio, chat):
    chat_data = chat.jsonify()
    sio.emit('chat_renamed', chat_data, room=chat_data['id'])

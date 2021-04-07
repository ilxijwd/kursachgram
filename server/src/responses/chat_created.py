def chat_created(sio, chat, room_id):
    sio.emit('chat_created', {'chat': chat.jsonify()}, room=room_id)

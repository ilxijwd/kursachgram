def chats(sio, sid, user_chats):
    sio.emit('chats', list(map(lambda c: c.jsonify(), user_chats)), room=sid)

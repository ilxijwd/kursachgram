def user_offline(sio, sid, user_id):
    sio.emit('user_offline', {'id': user_id}, skip_sid=sid)

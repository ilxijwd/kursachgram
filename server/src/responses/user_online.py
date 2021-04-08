def user_online(sio, sid, user_id):
    sio.emit('user_online', {'id': user_id}, skip_sid=sid)

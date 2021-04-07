def user_online(sio, sid, email):
    sio.emit('user_online', {'email': email}, skip_sid=sid)

def logged_in(sio, sid, token, user):
    sio.emit('logged_in', {'token': token, 'user': user}, room=sid)

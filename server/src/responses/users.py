def users(sio, sid, registered_users):
    sio.emit('users', list(map(lambda u: u.jsonify(), registered_users)), room=sid)

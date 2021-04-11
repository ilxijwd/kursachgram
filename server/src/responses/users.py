def users(sio, sid, online_users):
    sio.emit('users', list(map(lambda u: u.jsonify(), online_users)), room=sid)

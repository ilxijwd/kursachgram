def users(sio, sid, users_list):
    sio.emit('users', list(map(lambda u: u.jsonify(), users_list)), room=sid)

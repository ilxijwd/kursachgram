def me(sio, sid, user):
    sio.emit('me', user.jsonify(), room=sid)

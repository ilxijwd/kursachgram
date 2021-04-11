def user_offline(sio, sid, user):
    sio.emit('user_offline', user.jsonify(), skip_sid=sid)

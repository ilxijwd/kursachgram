def user_online(sio, sid, user):
    sio.emit('user_online', user.jsonify(), skip_sid=sid)

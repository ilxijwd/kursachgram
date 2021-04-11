def logged_in(sio, sid, token, user):
    user_data = user.jsonify()
    user_data['token'] = token
    sio.emit('logged_in', user_data, room=sid)

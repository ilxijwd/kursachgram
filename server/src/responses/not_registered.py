def not_registered(sio, sid):
    sio.emit('not_registered', room=sid)

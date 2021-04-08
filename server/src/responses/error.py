def error(sio, sid, error_code, skip_sid=-1):
    sio.emit('error', {'code': error_code}, room=sid, skip_sid=skip_sid)

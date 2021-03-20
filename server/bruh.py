import socketio
from eventlet import wsgi, listen

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
app = socketio.WSGIApp(sio)


@sio.event
def connect(sid, environ, auth):
    print("Accepted new connection", sid, environ, auth)


wsgi.server(listen(('', 8000)), app)

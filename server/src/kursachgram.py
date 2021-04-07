import importlib
from os import path, walk

import socketio
from eventlet import wsgi, listen


events_dir_path = path.join(path.dirname(__file__), 'events')
_, _, event_modules_filenames = next(walk(events_dir_path))
event_modules = list(map(importlib.import_module, list(map(lambda x: 'events.' + x[:-3], event_modules_filenames))))

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins='*')
for module in event_modules:
    if hasattr(module, 'register_event'):
        getattr(module, 'register_event')(sio)
    else:
        print(f'[sio] module named "{module.__name__}" has no "register_event" function')

app = socketio.WSGIApp(sio)
wsgi.server(listen(('', 8000)), app)

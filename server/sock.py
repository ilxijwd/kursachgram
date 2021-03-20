from flask_socketio import SocketIO
from kursachgram import create_app

socketio = SocketIO()


@socketio.on("connect")
def handle_message(data):
    print(data)


socketio.run(create_app())

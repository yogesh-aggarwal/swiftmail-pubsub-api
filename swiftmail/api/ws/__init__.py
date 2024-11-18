from flask_socketio import SocketIO

from .handlers.connect import on_connect
from .handlers.inbox import on_inbox


def init_websockets(app):
    socketio = SocketIO(app, cors_allowed_origins="*", path="/ws")

    @socketio.on("connect")
    def _():
        on_connect()

    @socketio.on("inbox")
    def _():
        on_inbox()

    return socketio

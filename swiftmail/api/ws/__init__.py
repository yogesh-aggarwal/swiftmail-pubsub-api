from flask import g
from flask_socketio import SocketIO, emit, disconnect

from swiftmail.api.middlewares.auth import get_user_from_request
from swiftmail.api.models.digest import Digest
from swiftmail.core.utils import generate_id
import time


def init_websockets(app):
    socketio = SocketIO(app, cors_allowed_origins="*", path="/ws")

    @socketio.on("connect")
    def _():
        g.user = get_user_from_request()
        if not g.user:
            disconnect()
            return

        print("Connected successfully as ", g.user)
        emit("connected", {"message": f"Connected successfully as {g.user.email}"})

    return socketio

from flask import g
from flask_socketio import disconnect, emit

from swiftmail.api.middlewares.auth import get_user_from_request


def on_connect():
    g.user = get_user_from_request()
    if not g.user:
        disconnect()
        return

    print("Connected successfully as ", g.user)
    emit("connected", {"message": f"Connected successfully as {g.user.email}"})

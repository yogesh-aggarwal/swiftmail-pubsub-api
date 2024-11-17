import eventlet
import logging

eventlet.monkey_patch()

from flask import Flask
from flask_cors import CORS

from swiftmail.core.constants import ALLOWED_ORIGINS, PORT
from swiftmail.api.rest.routes import root_router
from swiftmail.api.ws import init_websockets

# Disable Werkzeug logging
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)

# Disable Engine.IO logging
engineio_logger = logging.getLogger("engineio")
engineio_logger.setLevel(logging.ERROR)

# Disable Socket.IO logging
socketio_logger = logging.getLogger("socketio")
socketio_logger.setLevel(logging.ERROR)

app = Flask(__name__)
app.logger.disabled = True
CORS(app, origins="*" or ALLOWED_ORIGINS)

app.register_blueprint(root_router, url_prefix="/")

socketio = init_websockets(app)


def start_server():
    socketio.run(
        app,
        host="0.0.0.0",
        port=PORT,
        debug=True,
        log_output=False,  # Disable Socket.IO server logs
    )

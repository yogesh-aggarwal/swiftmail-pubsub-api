from flask import Flask
from flask_cors import CORS

from swiftmail.core.constants import ALLOWED_ORIGINS, PORT
from swiftmail.api.rest.routes import root_router

app = Flask(__name__)
app.logger.disabled = True
CORS(app, origins="*" or ALLOWED_ORIGINS)

app.register_blueprint(root_router, url_prefix="/")


def start_server():
    app.run(
        host="0.0.0.0",
        port=PORT,
        debug=True,
        log_output=False,  # Disable Socket.IO server logs
    )

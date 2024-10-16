import uvicorn
from asgiref.wsgi import WsgiToAsgi
from flask import Flask
from flask_cors import CORS

from swiftmail.core.constants import ALLOWED_ORIGINS, PORT

from .routes import root_router

app = Flask(__name__)
CORS(app, origins="*" or ALLOWED_ORIGINS)

app.register_blueprint(root_router, url_prefix="/")


def start_server():
    asgi_app = WsgiToAsgi(app)
    uvicorn.run(asgi_app, host="0.0.0.0", port=PORT, log_level="info")

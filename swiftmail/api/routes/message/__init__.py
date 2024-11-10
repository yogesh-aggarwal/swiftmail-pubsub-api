from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

from .reply import reply
from .resummarize import resummarize

message_router = Blueprint("message_router", __name__)

# Middlewares
message_router.before_request(firebase_auth_middleware)

# Routes
message_router.add_url_rule("/reply", view_func=reply, methods=["POST"])
message_router.add_url_rule("/resummarize", view_func=resummarize, methods=["PATCH"])


@message_router.route("/")
def index():
    return "OK", 200

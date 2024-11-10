from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

message_router = Blueprint("message_router", __name__)

# Middlewares
message_router.before_request(firebase_auth_middleware)


@message_router.route("/")
def index():
    return "OK", 200

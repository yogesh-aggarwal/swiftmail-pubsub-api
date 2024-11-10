from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

notification_router = Blueprint("notification_router", __name__)

# Middlewares
notification_router.before_request(firebase_auth_middleware)


@notification_router.route("/")
def index():
    return "OK", 200

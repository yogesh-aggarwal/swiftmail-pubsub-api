from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

from .import_inbox import import_inbox

user_router = Blueprint("user_router", __name__)

# Middlewares
user_router.before_request(firebase_auth_middleware)

# Routes
user_router.add_url_rule("/import-inbox", view_func=import_inbox, methods=["POST"])


@user_router.route("/")
def index():
    return "OK", 200

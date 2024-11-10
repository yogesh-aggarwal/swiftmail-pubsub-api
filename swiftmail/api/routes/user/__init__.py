from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

user_router = Blueprint("user_router", __name__)

# Middlewares
user_router.before_request(firebase_auth_middleware)


@user_router.route("/")
def index():
    return "OK", 200

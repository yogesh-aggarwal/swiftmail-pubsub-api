from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

thread_router = Blueprint("thread_router", __name__)

# Middlewares
thread_router.before_request(firebase_auth_middleware)


@thread_router.route("/")
def index():
    return "OK", 200

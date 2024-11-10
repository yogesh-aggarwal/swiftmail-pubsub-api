from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

digest_router = Blueprint("digest_router", __name__)

# Middlewares
digest_router.before_request(firebase_auth_middleware)


@digest_router.route("/")
def index():
    return "OK", 200

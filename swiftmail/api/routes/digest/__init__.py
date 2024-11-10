from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

from .create import create

digest_router = Blueprint("digest_router", __name__)

# Middlewares
digest_router.before_request(firebase_auth_middleware)


@digest_router.route("/")
def index():
    return "OK", 200


digest_router.add_url_rule("/create", view_func=create, methods=["POST"])

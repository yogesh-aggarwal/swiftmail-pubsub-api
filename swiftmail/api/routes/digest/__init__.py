from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

from .create import create
from .delete import delete
from .update import update

digest_router = Blueprint("digest_router", __name__)

# Middlewares
digest_router.before_request(firebase_auth_middleware)


@digest_router.route("/")
def index():
    return "OK", 200


digest_router.add_url_rule("/create", view_func=create, methods=["POST"])
digest_router.add_url_rule("/delete", view_func=delete, methods=["DELETE"])
digest_router.add_url_rule("/update", view_func=update, methods=["PATCH"])

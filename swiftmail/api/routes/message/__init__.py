from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

from .archive import archive
from .category import category
from .delete import delete
from .label import label
from .priority import priority
from .reply import reply
from .resummarize import resummarize

message_router = Blueprint("message_router", __name__)

# Middlewares
message_router.before_request(firebase_auth_middleware)

# Routes
message_router.add_url_rule("/archive", view_func=archive, methods=["PATCH"])
message_router.add_url_rule("/category", view_func=category, methods=["PATCH"])
message_router.add_url_rule("/delete", view_func=delete, methods=["DELETE"])
message_router.add_url_rule("/label", view_func=label, methods=["PATCH"])
message_router.add_url_rule("/reply", view_func=reply, methods=["POST"])
message_router.add_url_rule("/priority", view_func=priority, methods=["PATCH"])
message_router.add_url_rule("/resummarize", view_func=resummarize, methods=["PATCH"])


@message_router.route("/")
def index():
    return "OK", 200

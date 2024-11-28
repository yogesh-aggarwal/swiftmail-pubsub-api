from flask import Blueprint

from .new_message import new_message
from .import_inbox import import_inbox
from swiftmail.api.middlewares.auth import firebase_auth_middleware
from .reply_message import reply_message

queue_router = Blueprint("queue_router", __name__)

# Middlewares
queue_router.before_request(firebase_auth_middleware)

queue_router.add_url_rule("/new-message", view_func=new_message, methods=["POST"])
queue_router.add_url_rule("/import-inbox", view_func=import_inbox, methods=["POST"])
queue_router.add_url_rule("/reply", view_func=reply_message, methods=["POST"])

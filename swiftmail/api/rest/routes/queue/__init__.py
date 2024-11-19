from flask import Blueprint

from .new_message import new_message
from .import_messages import import_messages
from swiftmail.api.middlewares.auth import firebase_auth_middleware

queue_router = Blueprint("queue_router", __name__)

# Middlewares
queue_router.before_request(firebase_auth_middleware)

queue_router.add_url_rule("/new-message", view_func=new_message, methods=["POST"])
queue_router.add_url_rule("/import", view_func=import_messages, methods=["POST"])

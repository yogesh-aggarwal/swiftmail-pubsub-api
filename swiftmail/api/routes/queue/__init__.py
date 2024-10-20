from flask import Blueprint

from .new_message import new_message

queue_router = Blueprint("queue_router", __name__)

queue_router.add_url_rule("/new-message", view_func=new_message, methods=["POST"])

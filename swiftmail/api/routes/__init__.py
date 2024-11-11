from flask import Blueprint, redirect

from .auth import auth_router
from .dashboard import dashboard_router
from .digest import digest_router
from .message import message_router
from .notification import notification_router
from .queue import queue_router
from .template import template_router
from .thread import thread_router
from .user import user_router

root_router = Blueprint("root_router", __name__)

root_router.register_blueprint(auth_router, url_prefix="/auth")
root_router.register_blueprint(dashboard_router, url_prefix="/dashboard")
root_router.register_blueprint(digest_router, url_prefix="/digest")
root_router.register_blueprint(message_router, url_prefix="/message")
root_router.register_blueprint(notification_router, url_prefix="/notification")
root_router.register_blueprint(queue_router, url_prefix="/queue")
root_router.register_blueprint(template_router, url_prefix="/template")
root_router.register_blueprint(thread_router, url_prefix="/thread")
root_router.register_blueprint(user_router, url_prefix="/user")


@root_router.route("/")
def index():
    return redirect("/health")


@root_router.get("/health")
def health():
    return "OK", 200

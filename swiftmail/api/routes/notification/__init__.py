from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware
from swiftmail.api.routes.notification.dismiss import dismiss

notification_router = Blueprint("notification_router", __name__)

# Middlewares
notification_router.before_request(firebase_auth_middleware)


# Routes
notification_router.add_url_rule("/dismiss", view_func=dismiss, methods=["PATCH"])


@notification_router.route("/")
def index():
    return "OK", 200

from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

dashboard_router = Blueprint("dashboard_router", __name__)

# Middlewares
dashboard_router.before_request(firebase_auth_middleware)


@dashboard_router.route("/")
def index():
    return "OK", 200

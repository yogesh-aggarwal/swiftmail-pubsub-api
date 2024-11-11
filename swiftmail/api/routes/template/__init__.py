from flask import Blueprint

from swiftmail.api.middlewares.auth import firebase_auth_middleware

from .generate import generate

template_router = Blueprint("template_router", __name__)

# Middlewares
template_router.before_request(firebase_auth_middleware)

# Routes
template_router.add_url_rule("/generate", view_func=generate, methods=["POST"])


@template_router.route("/")
def index():
    return "OK", 200

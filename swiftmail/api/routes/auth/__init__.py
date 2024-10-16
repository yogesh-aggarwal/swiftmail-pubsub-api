from flask import Blueprint

from .google import google_auth_router
from .signup import signup

auth_router = Blueprint("auth_router", __name__)

auth_router.register_blueprint(google_auth_router, url_prefix="/google")

auth_router.add_url_rule("/signup", view_func=signup, methods=["POST"])

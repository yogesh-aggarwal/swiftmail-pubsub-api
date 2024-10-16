import os

from flask import Blueprint

from .auth_url import auth_url
from .callback import callback

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

google_auth_router = Blueprint("google_auth_router", __name__)

google_auth_router.add_url_rule("/auth_url", view_func=auth_url, methods=["GET"])
google_auth_router.add_url_rule("/callback", view_func=callback, methods=["POST"])

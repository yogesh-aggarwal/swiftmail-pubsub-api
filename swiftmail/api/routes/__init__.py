from flask import Blueprint, redirect

from .auth import auth_router

root_router = Blueprint("root_router", __name__)

root_router.register_blueprint(auth_router, url_prefix="/auth")


@root_router.route("/")
def index():
    return redirect("/health")


@root_router.get("/health")
def health():
    return "OK", 200

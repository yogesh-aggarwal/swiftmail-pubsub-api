from functools import wraps

from flask import jsonify, request, g
from flask_socketio import disconnect, emit
from urllib.parse import parse_qs

from swiftmail.api.models.user import User
from swiftmail.core.firebase import auth


def _handle_preflight():
    response = jsonify({"message": "CORS preflight"})
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add(
        "Access-Control-Allow-Headers",
        "Authorization, Content-Type",
    )
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response


def _extract_firebase_token():
    # For WebSocket connections, check URL parameters
    if hasattr(request, "environ") and "wsgi.url_scheme" in request.environ:
        query_string = request.environ.get("QUERY_STRING", "")
        params = parse_qs(query_string)
        token = params.get("token", [None])[0]
        if token:
            return token

    # For regular HTTP requests, check Authorization header
    firebase_auth_token = request.headers.get("Authorization")
    if firebase_auth_token:
        return firebase_auth_token.replace("Bearer ", "")

    return None


def _fetch_user_from_firebase_token(firebase_auth_token) -> User | None:
    try:
        user = auth.verify_id_token(firebase_auth_token)
        user_email = user["email"]

        user = User.get_from_email(user_email)
        return user
    except Exception:
        print("Rejected request with invalid Firebase token or user not found")

    return None


def get_user_from_request() -> User | None:
    firebase_auth_token = _extract_firebase_token()
    if not firebase_auth_token:
        return None

    user = _fetch_user_from_firebase_token(firebase_auth_token)
    return user


def firebase_auth_middleware():
    if request.method == "OPTIONS":
        return _handle_preflight()

    user = get_user_from_request()
    if not user:
        return jsonify({"message": "unauthorized"}), 401

    setattr(request, "user", user)

    return user


def firebase_auth_middleware_wrapped(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = firebase_auth_middleware()
        if response is not None:
            return response

        return func(*args, **kwargs)

    return wrapper

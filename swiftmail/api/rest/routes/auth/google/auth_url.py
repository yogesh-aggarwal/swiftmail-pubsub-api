from flask import jsonify

from swiftmail.api.middlewares.auth import firebase_auth_middleware_wrapped
from swiftmail.services.mail.gmail import Gmail


@firebase_auth_middleware_wrapped
def auth_url():
    mail = Gmail()
    url = mail.get_oauth_authorization_url()

    return jsonify({"message": "success", "url": url}), 200

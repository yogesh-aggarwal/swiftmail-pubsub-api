from flask import jsonify, request
from pydantic import BaseModel, Field

from swiftmail.api.models.user import User


class SignupRequestBody(BaseModel):
    uid: str = Field(..., alias="uid")
    name: str = Field(..., alias="name")
    email: str = Field(..., alias="email")
    dp: str = Field(..., alias="dp")
    password: str = Field(..., alias="password")


def signup():
    # Step 1: Validate body
    try:
        body = SignupRequestBody.model_validate(request.json)
    except:
        return jsonify({"message": "invalid_body_content"}), 403

    # Step 2: Check if user already exists
    existing_user = User.get_from_email(body.email)
    if existing_user:
        return jsonify({"message": "user_already_exists"}), 409

    # Step 3: Create user
    try:
        User.create(
            id=body.uid,
            email=body.email,
            name=body.name,
            dp=body.dp,
            password=body.password,
        )
    except:
        return jsonify({"message": "internal_server_error"}), 500

    return jsonify({"message": "success"}), 200

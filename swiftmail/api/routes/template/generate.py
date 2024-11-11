from flask import jsonify, request
from pydantic import BaseModel, Field


class RequestBody(BaseModel):
    prompt: str = Field(..., alias="prompt")


def generate():
    # Step 1: Validate body
    try:
        body = RequestBody.model_validate(request.json)
    except:
        return jsonify({"message": "invalid_body_content"}), 403

    # Step 2: Generate template
    try:
        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"message": "internal_server_error"}), 500

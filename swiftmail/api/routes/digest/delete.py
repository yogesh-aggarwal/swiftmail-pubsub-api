from flask import jsonify, request
from pydantic import BaseModel, Field

from swiftmail.api.models.digest import Digest
from swiftmail.api.models.user import User


class RequestBody(BaseModel):
    digest_id: str = Field(..., alias="digest_id")
    apply_to_existing: bool | None = Field(False, alias="apply_to_existing")


def delete():
    user: User = getattr(request, "user", None)  # type:ignore

    # Step 1: Validate body
    try:
        body = RequestBody.model_validate(request.json)
    except:
        return jsonify({"message": "invalid_body_content"}), 403

    # Step 2: Check if user is the owner of the digest
    digest = Digest.get_by_id(body.digest_id)
    if not digest:
        return jsonify({"message": "digest_not_found"}), 404
    if digest.user_id != user.id:
        return jsonify({"message": "unauthorized"}), 403

    # Step 2: Update inbox
    try:
        # TODO: Apply to existing emails

        return jsonify({"message": "success"}), 200
    except Exception as e:
        return jsonify({"message": "internal_server_error"}), 500

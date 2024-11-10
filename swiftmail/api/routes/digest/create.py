import time
from flask import jsonify, request
from pydantic import BaseModel, Field

from swiftmail.api.models.user import User
from swiftmail.api.models.digest import Digest
from swiftmail.core.utils import generate_id


class RequestBody(BaseModel):
    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")
    apply_to_existing: bool = Field(False, alias="apply_to_existing")


def create():
    user: User = getattr(request, "user", None)  # type:ignore

    # Step 1: Validate body
    try:
        body = RequestBody.model_validate(request.json)
    except:
        return jsonify({"message": "invalid_body_content"}), 403

    # Step 2: Create digest
    try:
        digest = Digest(
            #
            id=generate_id(),
            user_id=user.id,
            date_created=int(time.time()),
            date_updated=int(time.time()),
            #
            title=body.title,
            description=body.description,
        )
        digest.create()

        # TODO: Apply to existing emails

        return jsonify({"message": "success", "data": {"id": digest.id}}), 200
    except Exception as e:
        return jsonify({"message": "internal_server_error"}), 500

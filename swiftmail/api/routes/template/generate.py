from flask import jsonify, request
from pydantic import BaseModel, Field

from swiftmail.api.models.user import User
from swiftmail.factory.prompts import PromptFactory
from swiftmail.services.llm.utils import get_llm_from_string


class RequestBody(BaseModel):
    prompt: str = Field(..., alias="prompt")


class GenerateTemplateResult(BaseModel):
    html_content: str = Field(..., alias="html_content")


def generate():
    user: User = getattr(request, "user", None)  # type:ignore

    # Step 1: Validate body
    try:
        body = RequestBody.model_validate(request.json)
    except:
        return jsonify({"message": "invalid_body_content"}), 403

    # Step 2: Generate template
    llm = get_llm_from_string(user.data.preferences.ai.model)
    prompt = PromptFactory.generate_template(
        user_name=user.name,
        user_email=user.email,
        user_bio=user.data.preferences.ai.self_description,
        template_description=body.prompt,
    )
    res = llm.run(prompt, temperature=0)
    if not res:
        return jsonify({"message": "internal_server_error"}), 500

    html_content = GenerateTemplateResult.model_validate_json(res).html_content

    return jsonify({"message": "success", "content": html_content}), 200

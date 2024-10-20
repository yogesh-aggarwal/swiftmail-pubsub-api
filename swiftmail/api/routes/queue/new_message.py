from rich import print

from flask import request

from swiftmail.api.models.message import Message
from swiftmail.api.models.user import User, UserPreferences
from swiftmail.factory.prompts import PromptFactory
from swiftmail.services.llm.utils import get_llm_from_string


def _process_message(
    subject: str,
    html_content: str,
    user_prefs: UserPreferences,
) -> Message | None:
    llm_model = get_llm_from_string(user_prefs.ai.model)
    llm_prompt = PromptFactory.email_segregation(
        email_subject=subject,
        email_html_content=html_content,
        user_bio=user_prefs.ai.self_description,
        user_defined_priorities=user_prefs.inbox.priorities,
        user_defined_priority_rules=user_prefs.inbox.priority_rules,
        user_defined_labels=user_prefs.inbox.labels,
        user_defined_label_rules=user_prefs.inbox.label_rules,
        user_defined_categories=user_prefs.inbox.categories,
        user_defined_category_rules=user_prefs.inbox.category_rules,
        user_defined_spam_words=user_prefs.inbox.spam_words,
        user_defined_spam_rules=user_prefs.inbox.spam_rules,
        user_defined_unsubscribe_words=user_prefs.inbox.unsubscribe_words,
        user_defined_unsubscribe_rules=user_prefs.inbox.unsubscribe_rules,
        enforce_not_spam=False,
    )

    print(llm_model, llm_prompt)


def new_message():
    user: User = getattr(request, "user", None)  # type:ignore
    print(user)

    _process_message(
        subject="Test",
        html_content="Test",
        user_prefs=user.data.preferences,
    )

    return "OK", 200

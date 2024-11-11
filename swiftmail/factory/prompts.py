import json

from swiftmail.services.llm import LLMMessage, LLMPrompt


class PromptFactory:
    @staticmethod
    def email_summarize(*, html_content: str):
        with open("assets/email_summarize/system.txt") as f:
            system_prompt = f.read()
        with open("assets/email_summarize/user.txt") as f:
            user_prompt = f.read().strip()
            user_prompt = user_prompt.format(
                input_json=json.dumps({"html_content": html_content})
            )

        return LLMPrompt(
            "Email Summarize",
            [
                LLMMessage("system", system_prompt),
                LLMMessage("user", user_prompt),
            ],
        )

    @staticmethod
    def email_digest_segregate(
        *,
        # Digests
        user_digest_ids: list[str],
        user_digest_titles: list[str],
        user_digest_descriptions: list[str],
        # Emails
        email_subject: str,
        email_content: str,
    ):
        if (
            len(user_digest_ids) != len(user_digest_titles)
            or len(user_digest_ids) != len(user_digest_descriptions)
            or len(user_digest_titles) != len(user_digest_descriptions)
        ):
            raise ValueError("All lists must be of the same length")

        with open("assets/email_digest_segregate/system.txt") as f:
            system_prompt = f.read()
        with open("assets/email_digest_segregate/user.txt") as f:
            user_prompt = f.read().strip()
            user_prompt = user_prompt.format(
                input_json=json.dumps(
                    {
                        "digests": [
                            {
                                "id": user_digest_ids[i],
                                "title": user_digest_titles[i],
                                "description": user_digest_descriptions[i],
                            }
                            for i in range(len(user_digest_ids))
                        ],
                        "emails": {
                            "subject": email_subject,
                            "html_content": email_content,
                        },
                    }
                ),
            )

        return LLMPrompt(
            "Email Digest Segregate",
            [
                LLMMessage("system", system_prompt),
                LLMMessage("user", user_prompt),
            ],
        )

    @staticmethod
    def email_segregation(
        *,
        # User about
        user_bio: str,
        # Email
        email_subject: str,
        email_html_content: str,
        # Config
        enforce_not_spam: bool,
        # Priority
        user_defined_priorities: list[str],
        user_defined_priority_rules: list[str],
        # Labels
        user_defined_labels: list[str],
        user_defined_label_rules: list[str],
        # Spam
        user_defined_spam_words: list[str],
        user_defined_spam_rules: list[str],
        # Unsubscribe
        user_defined_unsubscribe_words: list[str],
        user_defined_unsubscribe_rules: list[str],
        # Categories
        user_defined_categories: list[str],
        user_defined_category_rules: list[str],
    ):
        with open("assets/email_segregate/system.txt") as f:
            system_prompt = f.read()
        with open("assets/email_segregate/user.txt") as f:
            user_prompt = f.read().strip()
            user_prompt = user_prompt.format(
                input_json=json.dumps(
                    {
                        "user_bio": user_bio,
                        "email_subject": email_subject,
                        "email_html_content": email_html_content,
                        "enforce_not_spam": enforce_not_spam,
                        "user_defined_priorities": user_defined_priorities,
                        "user_defined_priority_rules": user_defined_priority_rules,
                        "user_defined_labels": user_defined_labels,
                        "user_defined_label_rules": user_defined_label_rules,
                        "user_defined_spam_words": user_defined_spam_words,
                        "user_defined_spam_rules": user_defined_spam_rules,
                        "user_defined_unsubscribe_words": user_defined_unsubscribe_words,
                        "user_defined_unsubscribe_rules": user_defined_unsubscribe_rules,
                        "user_defined_categories": user_defined_categories,
                        "user_defined_category_rules": user_defined_category_rules,
                    }
                ),
            )

        return LLMPrompt(
            "Email Segregation",
            [
                LLMMessage("system", system_prompt),
                LLMMessage("user", user_prompt),
            ],
        )

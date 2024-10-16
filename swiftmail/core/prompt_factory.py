from swiftmail.services.llm import LLMMessage, LLMPrompt


class PromptFactory:
    @staticmethod
    def email_segregation(
        *,
        user_bio: str,
        email_html_content: str,
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
            user_prompt = f.read()

        return LLMPrompt(
            "Email Segregation",
            [
                LLMMessage("system", system_prompt),
                LLMMessage("user", user_prompt),
            ],
        )

import rich
from swiftmail.jobs.email.models import (
    ProcessEmailJobData,
    EmailClassificationResult,
    EmailDigestResult,
    EmailSummaryResult,
    EmailEmbeddingResult,
    ThreadSummaryResult,
)
from swiftmail.factory.prompts import PromptFactory
from swiftmail.services.llm.utils import get_llm_from_string
from swiftmail.services.embedding.utils import get_embedding_from_string
from swiftmail.api.models.digest import Digest
from swiftmail.services.llm import LLMService
import json


class EmailProcessor:
    """Base class for email processors"""

    def __init__(self, job_data: ProcessEmailJobData):
        self.job_data = job_data
        self.user_prefs = job_data.user.data.preferences


class EmbeddingProcessor(EmailProcessor):
    def process(self) -> EmailEmbeddingResult:
        embedding_service = get_embedding_from_string("openai")
        text = f"{self.job_data.email.subject}\n\n{self.job_data.email.html_content}"
        embeddings = embedding_service.embed([text])
        return EmailEmbeddingResult(embedding=embeddings[0])


class ClassificationProcessor(EmailProcessor):
    def process(self) -> EmailClassificationResult:
        llm_model = get_llm_from_string(self.user_prefs.ai.model)

        llm_prompt = PromptFactory.email_segregation(
            email_subject=self.job_data.email.subject,
            email_html_content=self.job_data.email.html_content,
            user_bio=self.user_prefs.ai.self_description,
            user_defined_priorities=self.user_prefs.inbox.priorities,
            user_defined_priority_rules=self.user_prefs.inbox.priority_rules,
            user_defined_labels=self.user_prefs.inbox.labels,
            user_defined_label_rules=self.user_prefs.inbox.label_rules,
            user_defined_categories=self.user_prefs.inbox.categories,
            user_defined_category_rules=self.user_prefs.inbox.category_rules,
            user_defined_spam_words=self.user_prefs.inbox.spam_words,
            user_defined_spam_rules=self.user_prefs.inbox.spam_rules,
            user_defined_unsubscribe_words=self.user_prefs.inbox.unsubscribe_words,
            user_defined_unsubscribe_rules=self.user_prefs.inbox.unsubscribe_rules,
            enforce_not_spam=False,
        )

        res = llm_model.run(llm_prompt, temperature=0)
        if not res:
            return EmailClassificationResult(
                spam=False,
                priority="Low",
                labels=[],
                categories=[],
                unsubscribe_link=None,
                keywords=[],
            )

        return EmailClassificationResult.model_validate_json(res)


class DigestProcessor(EmailProcessor):
    def process(self) -> EmailDigestResult:
        digests = Digest.get_by_user_id(self.job_data.user.id)
        llm_model = get_llm_from_string(self.user_prefs.ai.model)

        llm_prompt = PromptFactory.email_digest_segregate(
            email_subject=self.job_data.email.subject,
            email_content=self.job_data.email.html_content,
            user_digest_ids=[d.id for d in digests],
            user_digest_titles=[d.title for d in digests],
            user_digest_descriptions=[d.description for d in digests],
        )

        res = llm_model.run(llm_prompt, temperature=0)
        if not res:
            return EmailDigestResult(digests=[])

        return EmailDigestResult.model_validate_json(res)


class SummaryProcessor(EmailProcessor):
    def process(self) -> EmailSummaryResult:
        llm_model = get_llm_from_string(self.user_prefs.ai.model)

        llm_prompt = PromptFactory.email_summarize(
            html_content=self.job_data.email.html_content
        )

        res = llm_model.run(llm_prompt, temperature=0)
        if not res:
            return EmailSummaryResult(summary="")

        return EmailSummaryResult.model_validate_json(res)


class ThreadSummaryProcessor(EmailProcessor):
    def process(self, message_summaries: list[str]) -> ThreadSummaryResult:
        """Process the thread summaries and return a consolidated summary"""
        if not message_summaries:
            return ThreadSummaryResult(summary="")

        llm_model = get_llm_from_string(self.user_prefs.ai.model)
        prompt = PromptFactory.thread_summarize(message_summaries=message_summaries)

        res = llm_model.run(prompt, temperature=0)
        if not res:
            return ThreadSummaryResult(summary="\n".join(message_summaries))

        try:
            result = json.loads(res)
            return ThreadSummaryResult(summary=result["thread_summary"])
        except (json.JSONDecodeError, KeyError):
            # Fallback to simple concatenation if LLM fails
            return ThreadSummaryResult(summary="\n".join(message_summaries))

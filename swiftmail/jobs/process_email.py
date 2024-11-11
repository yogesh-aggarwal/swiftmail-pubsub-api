from concurrent.futures import ThreadPoolExecutor
from typing import Any
import time

from pydantic import BaseModel
from rich import print

from swiftmail.api.models.digest import Digest
from swiftmail.api.models.data import Data, DataType
from swiftmail.core.utils import generate_id
from swiftmail.api.models.message import (
    Message,
    MessageEmailData,
    MessageFlags,
    MessageReminders,
)
from swiftmail.api.models.user import User
from swiftmail.factory.prompts import PromptFactory
from swiftmail.services.llm.utils import get_llm_from_string


class ProcessEmailJobData(BaseModel):
    email: MessageEmailData
    user: User


# -----------------------------------------------------------------------------


class SegregatedEmailToDigestResult(BaseModel):
    digests: list[str]


def segregate_email_to_digest(
    job_data_dict: Any,
) -> SegregatedEmailToDigestResult:
    job_data = ProcessEmailJobData.model_validate(job_data_dict)

    subject = job_data.email.subject
    html_content = job_data.email.html_content
    user_prefs = job_data.user.data.preferences

    digests = Digest.get_by_user_id(job_data.user.id)

    llm_model = get_llm_from_string(user_prefs.ai.model)
    llm_prompt = PromptFactory.email_digest_segregate(
        # Email
        email_subject=subject,
        email_content=html_content,
        # Digests
        user_digest_ids=[digest.id for digest in digests],
        user_digest_titles=[digest.title for digest in digests],
        user_digest_descriptions=[digest.description for digest in digests],
    )
    res = llm_model.run(llm_prompt, temperature=0)
    if res is None:
        return SegregatedEmailToDigestResult(digests=[])

    return SegregatedEmailToDigestResult.model_validate_json(res)


# -----------------------------------------------------------------------------


class SummarizeEmailResult(BaseModel):
    summary: str


def summarize_email(job_data_dict: Any) -> SummarizeEmailResult:
    job_data = ProcessEmailJobData.model_validate(job_data_dict)

    subject = job_data.email.subject
    html_content = job_data.email.html_content
    user_prefs = job_data.user.data.preferences

    digests = Digest.get_by_user_id(job_data.user.id)

    llm_model = get_llm_from_string(user_prefs.ai.model)
    llm_prompt = PromptFactory.email_summarize(html_content=html_content)
    res = llm_model.run(llm_prompt, temperature=0)
    if res is None:
        return SummarizeEmailResult(summary="")

    return SummarizeEmailResult.model_validate_json(res)


# -----------------------------------------------------------------------------


class SegregatedEmailToClassificationResult(BaseModel):
    spam: bool
    priority: str
    labels: list[str]
    categories: list[str]
    unsubscribe_link: str | None


def segregate_email_to_classification(
    job_data_dict: Any,
) -> SegregatedEmailToClassificationResult:
    job_data = ProcessEmailJobData.model_validate(job_data_dict)

    subject = job_data.email.subject
    html_content = job_data.email.html_content
    user_prefs = job_data.user.data.preferences

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
    res = llm_model.run(llm_prompt, temperature=0)
    if res is None:
        return SegregatedEmailToClassificationResult(
            spam=False,
            priority="Low",
            labels=[],
            categories=[],
            unsubscribe_link=None,
        )

    return SegregatedEmailToClassificationResult.model_validate_json(res)


# -----------------------------------------------------------------------------


def process_email(job_data_str: str):
    job_data = ProcessEmailJobData.model_validate_json(job_data_str)

    jobs = []
    with ThreadPoolExecutor() as executor:
        jobs.append(executor.submit(summarize_email, job_data.model_dump()))
        jobs.append(executor.submit(segregate_email_to_digest, job_data.model_dump()))
        jobs.append(
            executor.submit(segregate_email_to_classification, job_data.model_dump())
        )
    results = [job.result() for job in jobs]

    summary, digests_result, classification_result = results

    print(results)

    message = Message(
        id=generate_id(),
        user_id=job_data.user.id,
        date_updated=int(time.time() * 1000),
        date_created=int(time.time() * 1000),
        flags=MessageFlags(
            is_archived=False,
            is_starred=False,
            is_trash=False,
            is_draft=False,
            is_sent=False,
            is_received=True,
            is_read=False,
            is_unread=True,
            is_deleted=False,
            is_junk=False,
            is_spam=classification_result.spam,
        ),
        reminders=MessageReminders(
            follow_up=[],
            forgetting=[],
            snoozed=[],
        ),
        email_data=job_data.email,
        summary=summary.summary,
        template=None,
        priorities=[classification_result.priority],
        categories=classification_result.categories,
        labels=classification_result.labels,
        digests=digests_result.digests,
    )
    message.create()

    data = Data(
        id=generate_id(),
        date_created=int(time.time() * 1000),
        type=DataType.EMAIL_RECEIVED,
        user_id=job_data.user.id,
        data={
            "priority": classification_result.priority,
            "labels": classification_result.labels,
            "categories": classification_result.categories,
            "digests": digests_result.digests,
            "summary_words": len(summary.summary.split()),
        },
    )
    data.create()

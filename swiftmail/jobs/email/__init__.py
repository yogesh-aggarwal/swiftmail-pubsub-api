import time
import json
from concurrent.futures import ThreadPoolExecutor

from swiftmail.api.models.data import Data, DataType
from swiftmail.api.models.message import Message, MessageReminders
from swiftmail.api.models.user import User
from swiftmail.api.models.thread import Thread, ThreadFlags
from swiftmail.core.utils import with_retry

from swiftmail.jobs.email.models import EmailClassificationResult, ProcessEmailJobData
from swiftmail.jobs.email.processors import (
    ClassificationProcessor,
    DigestProcessor,
    EmbeddingProcessor,
    SummaryProcessor,
    ThreadSummaryProcessor,
)


def _create_data_if_not_exists(
    user_id: str,
    priority: str,
    labels: list[str],
    categories: list[str],
    digests: list[str],
    summary_words: str,
    keywords: list[str],
    has_unsubscribe: bool,
):
    """Create a data if it doesn't exist"""
    data = Data(
        date_created=int(time.time() * 1000),
        type=DataType.EMAIL_RECEIVED,
        user_id=user_id,
        data={
            "priority": priority,
            "labels": labels,
            "categories": categories,
            "digests": digests,
            "summary_words": summary_words,
            "keywords": keywords,
            "has_unsubscribe": has_unsubscribe,
        },
    )
    data.create()
    return data


def _update_thread_summary(thread_id: str, user: User):
    """Update a thread's summary"""
    thread = Thread.get_by_id(thread_id)
    if thread is None:
        return

    thread.date_updated = int(time.time() * 1000)

    messages = Message.get_by_thread_id(thread_id)
    if not messages:
        thread.summary = ""
        thread.save()
        return

    summaries = [message.summary for message in messages if message.summary]

    if not summaries:
        thread.summary = ""
        thread.save()
        return

    first_message = messages[0]
    job_data = ProcessEmailJobData(email=first_message.email_data, user=user)

    summary_processor = ThreadSummaryProcessor(job_data)
    result = summary_processor.process(message_summaries=summaries)
    thread.summary = result.summary

    thread.save()


def _create_thread_if_not_exists(
    job_data: ProcessEmailJobData, classification_result: EmailClassificationResult
):
    """Create a thread if it doesn't exist"""
    thread = Thread.get_by_id(job_data.email.thread_id)
    if thread is not None:
        _update_thread_summary(thread.id, job_data.user)
        thread.update_snippet(job_data.email.snippet)
        return thread

    digests_result = DigestProcessor(job_data).process()

    thread = Thread(
        id=job_data.email.thread_id,
        user_id=str(job_data.user.id),
        date_updated=int(time.time() * 1000),
        date_created=int(time.time() * 1000),
        title=job_data.email.subject,
        description=job_data.email.snippet,
        thread_id=job_data.email.thread_id,
        flags=ThreadFlags(
            is_muted=False,
            is_read=False,
            is_starred=False,
            is_archived=False,
            is_spam=False,
            is_trash=False,
        ),
        summary="",  # Will be filled later by processing
        priority=classification_result.priority,
        categories=classification_result.categories,
        labels=classification_result.labels,
        digests=digests_result.digests,
    )
    thread.create()

    _update_thread_summary(thread.id, job_data.user)

    return thread


@with_retry(1)
def process_email(job_data_str: str):
    """Main email processing function"""
    job_data = ProcessEmailJobData.model_validate_json(job_data_str)

    if message := Message.get_by_id(job_data.email.message_id):
        print("Email already processed")
        return

    print("Processing email")

    # Initialize processors
    summary_processor = SummaryProcessor(job_data)
    embedding_processor = EmbeddingProcessor(job_data)
    classification_processor = ClassificationProcessor(job_data)

    # # Run all processing tasks in parallel
    # with ThreadPoolExecutor() as executor:
    #     future_summary = executor.submit(summary_processor.process)
    #     future_embedding = executor.submit(embedding_processor.process)
    #     future_classification = executor.submit(classification_processor.process)

    # # Get results
    # summary_result = future_summary.result()
    # embedding_result = future_embedding.result()
    # classification_result = future_classification.result()

    summary_result = summary_processor.process()
    embedding_result = embedding_processor.process()
    classification_result = classification_processor.process()

    # Store results
    message = Message(
        id=job_data.email.message_id,
        thread_id=job_data.email.thread_id,
        user_id=str(job_data.user.id),
        date_updated=int(time.time() * 1000),
        date_created=int(time.time() * 1000),
        reminders=MessageReminders(
            follow_up=[],
            forgetting=[],
            snoozed=[],
        ),
        email_data=job_data.email,
        summary=summary_result.summary,
        embedding=embedding_result.embedding,
        keywords=classification_result.keywords,
        unsubscribe_link=classification_result.unsubscribe_link,
    )
    message.create()

    thread = _create_thread_if_not_exists(job_data, classification_result)

    _create_data_if_not_exists(
        user_id=str(job_data.user.id),
        priority=thread.priority,
        labels=thread.labels,
        categories=thread.categories,
        digests=thread.digests,
        summary_words=summary_result.summary,
        keywords=message.keywords,
        has_unsubscribe=message.unsubscribe_link is not None,
    )

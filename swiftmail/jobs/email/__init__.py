import time
from concurrent.futures import ThreadPoolExecutor

from swiftmail.api.models.data import Data, DataType
from swiftmail.api.models.message import Message, MessageReminders
from swiftmail.core.utils import generate_id, with_retry

from .models import ProcessEmailJobData
from .processors import (
    ClassificationProcessor,
    DigestProcessor,
    EmbeddingProcessor,
    SummaryProcessor,
)


@with_retry(3)
def process_email(job_data_str: str):
    """Main email processing function"""
    job_data = ProcessEmailJobData.model_validate_json(job_data_str)

    # Initialize processors
    embedding_processor = EmbeddingProcessor(job_data)
    classification_processor = ClassificationProcessor(job_data)
    digest_processor = DigestProcessor(job_data)
    summary_processor = SummaryProcessor(job_data)

    # Run all processing tasks in parallel
    with ThreadPoolExecutor() as executor:
        future_embedding = executor.submit(embedding_processor.process)
        future_classification = executor.submit(classification_processor.process)
        future_digests = executor.submit(digest_processor.process)
        future_summary = executor.submit(summary_processor.process)

    # Get results
    embedding_result = future_embedding.result()
    classification_result = future_classification.result()
    digests_result = future_digests.result()
    summary_result = future_summary.result()

    # Store results
    message = Message(
        _id=generate_id(),
        user_id=job_data.user.id,
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

    data = Data(
        _id=generate_id(),
        date_created=int(time.time() * 1000),
        type=DataType.EMAIL_RECEIVED,
        user_id=job_data.user.id,
        data={
            "priority": classification_result.priority,
            "labels": classification_result.labels,
            "categories": classification_result.categories,
            "digests": digests_result.digests,
            "summary_words": len(summary_result.summary.split()),
            "keywords": classification_result.keywords,
            "has_unsubscribe": classification_result.unsubscribe_link is not None,
        },
    )
    data.create()
    return data

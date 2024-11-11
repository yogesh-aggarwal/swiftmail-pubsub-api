from flask import request

from swiftmail.api.models.message import MessageEmailData
from swiftmail.jobs.process_email import ProcessEmailJobData, process_email


def new_message():
    user: User = getattr(request, "user", None)  # type:ignore

    process_email(
        ProcessEmailJobData(
            email=MessageEmailData(
                subject="Sample Subject",
                html_content="<p>This is a test email content.</p>",
                message_id="sample_message_id",
                thread_id="sample_thread_id",
                from_email="from@example.com",
                to_email="to@example.com",
                cc_email="cc@example.com",
                bcc_email="bcc@example.com",
            ),
            user=user,
        ).model_dump_json()
    )

    return "OK", 200

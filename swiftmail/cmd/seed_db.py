import asyncio
from datetime import datetime

from swiftmail.api.models.dashboard import (
    Dashboard,
    DashboardSection,
    DashboardSectionStatusEnum,
)
from swiftmail.api.models.data import Data, DataType
from swiftmail.api.models.digest import Digest
from swiftmail.api.models.message import (
    Message,
    MessageEmailData,
    MessageFlags,
    MessageReminders,
)
from swiftmail.api.models.notification import Notification, NotificationStatus
from swiftmail.api.models.reminder import Reminder, ReminderState, ReminderType
from swiftmail.api.models.thread import Thread, ThreadFlags
from swiftmail.api.models.user import User


async def _setup_user(name: str, email: str, password: str):
    user = User.create(
        id=email,
        email=email,
        name=name,
        dp="https://picsum.photos/seed/yogeshdevaggarwal/200/200",
        password=password,
    )

    # Create related data for the user
    thread = Thread(
        id="thread1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp()),
        date_updated=int(datetime.now().timestamp()),
        title="Sample Thread",
        description="This is a sample thread",
        summary="Sample summary",
        thread_id="thread1",
        flags=ThreadFlags(
            is_muted=False,
            is_starred=False,
            is_trash=False,
            is_archived=False,
            is_read=False,
            is_unread=True,
            is_deleted=False,
            is_junk=False,
            is_spam=False,
        ),
    )
    thread.create()

    reminder = Reminder(
        id="reminder1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp()),
        date_updated=int(datetime.now().timestamp()),
        scheduled_at=int(datetime.now().timestamp() + 3600),  # 1 hour later
        time_zone="UTC",
        message_id="message1",
        thread_id="thread1",
        type=ReminderType.FOLLOW_UP,
        state=ReminderState.NOT_STARTED,
    )
    reminder.create()

    notification = Notification(
        id="notification1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp()),
        date_updated=int(datetime.now().timestamp()),
        date_delivered=None,
        date_dispatched=None,
        date_failed=None,
        title="Sample Notification",
        body="This is a sample notification",
        status=NotificationStatus.DISPATCHED,
    )
    notification.create()

    message = Message(
        id="message1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp()),
        date_updated=int(datetime.now().timestamp()),
        email_data=MessageEmailData(
            subject="Sample Subject",
            html_content="<p>This is a sample email content</p>",
            message_id="message1",
            thread_id="thread1",
            from_email="from@example.com",
            to_email="to@example.com",
            cc_email="cc@example.com",
            bcc_email="bcc@example.com",
        ),
        flags=MessageFlags(
            is_archived=False,
            is_starred=False,
            is_trash=False,
            is_draft=False,
            is_sent=True,
            is_received=True,
            is_read=False,
            is_unread=True,
            is_deleted=False,
            is_junk=False,
            is_spam=False,
        ),
        reminders=MessageReminders(follow_up=[], forgetting=[], snoozed=[]),
        summary="Sample summary",
        template=None,
        priorities=["high"],
        categories=["category1"],
        labels=["label1"],
        digests=["digest1"],
    )
    message.create()

    digest = Digest(
        id="digest1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp()),
        date_updated=int(datetime.now().timestamp()),
        title="Sample Digest",
        description="This is a sample digest",
    )
    digest.create()

    data = Data(
        id="data1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp()),
        type=DataType.EMAIL_RECEIVED,
        data={"key": "value"},
    )
    data.create()

    dashboard_section = DashboardSection(
        id="section1",
        date_updated=int(datetime.now().timestamp()),
        title="Sample Section",
        description="This is a sample section",
        status=DashboardSectionStatusEnum.READY,
        time_range_start=int(datetime.now().timestamp()),
        time_range_end=int(datetime.now().timestamp()),
        data={"key": "value"},
    )

    dashboard = Dashboard(
        id="dashboard1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp()),
        date_updated=int(datetime.now().timestamp()),
        sections={"section1": dashboard_section},
    )
    dashboard.create()


async def _setup_users():
    users = [
        ("Yogesh Aggarwal", "yogeshdevaggarwal@gmail.com", "12345678"),
    ]

    jobs = map(lambda x: _setup_user(*x), users)

    await asyncio.gather(*jobs)


def main():
    asyncio.run(_setup_users())

    print("Done!")


if __name__ == "__main__":
    main()

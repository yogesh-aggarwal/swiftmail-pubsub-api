import asyncio
import random
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

    reminder = Reminder(
        id="reminder1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp() * 1000),
        date_updated=int(datetime.now().timestamp() * 1000),
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
        date_created=int(datetime.now().timestamp() * 1000),
        date_updated=int(datetime.now().timestamp() * 1000),
        date_delivered=None,
        date_dispatched=None,
        date_failed=None,
        title="Sample Notification",
        body="This is a sample notification",
        status=NotificationStatus.DISPATCHED,
    )
    notification.create()

    digest = Digest(
        id=f"digest0",
        user_id=user.id,
        date_created=int(datetime.now().timestamp() * 1000),
        date_updated=int(datetime.now().timestamp() * 1000),
        title="Test emails",
        description="This digest contains test emails from any source",
    )
    digest.create()
    for i in range(1, 4):
        digest = Digest(
            id=f"digest{i}",
            user_id=user.id,
            date_created=int(datetime.now().timestamp() * 1000),
            date_updated=int(datetime.now().timestamp() * 1000),
            title=["College placements", "Funding updates", "SaaS updates"][i - 1],
            description="This is a sample digest",
        )
        digest.create()

    # Create related data for the user
    for i in range(1, 3):
        thread = Thread(
            id=f"thread{i}",
            user_id=user.id,
            date_created=int(datetime.now().timestamp() * 1000),
            date_updated=int(datetime.now().timestamp() * 1000),
            title=f"Sample Thread {i}",
            description=f"This is a sample thread {i}",
            summary="Sample summary",
            thread_id=f"thread{i}",
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

    for i in range(1, 20):
        message = Message(
            id=f"message{i}",
            user_id=user.id,
            date_created=int(datetime.now().timestamp() * 1000),
            date_updated=int(datetime.now().timestamp() * 1000),
            email_data=MessageEmailData(
                subject=f"Sample Subject {i}",
                html_content="<p>This is a sample email content</p>",
                message_id=f"message{i}",
                thread_id=f"thread{(i % 2) + 1}",
                from_email="from@example.com",
                to_email="to@example.com",
                cc_email="cc@example.com",
                bcc_email="bcc@example.com",
            ),
            flags=MessageFlags(
                is_archived=random.choice([True, False]),
                is_starred=random.choice([True, False]),
                is_trash=random.choice([True, False]),
                is_draft=random.choice([True, False]),
                is_sent=random.choice([True, False]),
                is_received=random.choice([True, False]),
                is_read=random.choice([True, False]),
                is_unread=random.choice([True, False]),
                is_deleted=random.choice([True, False]),
                is_junk=random.choice([True, False]),
                is_spam=random.choice([True, False]),
            ),
            reminders=MessageReminders(follow_up=[], forgetting=[], snoozed=[]),
            summary="Sample summary",
            template=None,
            priorities=["high"],
            categories=[
                random.choice(["Primary", "Social", "Promotions", "Updates", "Forums"])
            ],
            labels=[f"label{i}"],
            digests=[f"digest{random.choice([1, 2, 3])}"],
        )
        message.create()

    data = Data(
        id="data1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp() * 1000),
        type=DataType.EMAIL_RECEIVED,
        data={"key": "value"},
    )
    data.create()

    dashboard_section = DashboardSection(
        id="section1",
        date_updated=int(datetime.now().timestamp() * 1000),
        title="Sample Section",
        description="This is a sample section",
        status=DashboardSectionStatusEnum.READY,
        time_range_start=int(datetime.now().timestamp() * 1000),
        time_range_end=int(datetime.now().timestamp() * 1000),
        data={"key": "value"},
    )

    dashboard = Dashboard(
        id="dashboard1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp() * 1000),
        date_updated=int(datetime.now().timestamp() * 1000),
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

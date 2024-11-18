import asyncio
import random
import time
from datetime import datetime

from swiftmail.api.models.data import Data, DataType
from swiftmail.api.models.digest import Digest
from swiftmail.api.models.message import Message, MessageEmailData, MessageReminders
from swiftmail.api.models.notification import Notification, NotificationStatus
from swiftmail.api.models.reminder import Reminder, ReminderState, ReminderType
from swiftmail.api.models.thread import Thread, ThreadFlags
from swiftmail.api.models.user import User


async def _setup_user(name: str, email: str):
    # Create user with proper model structure
    user = User.create(
        id=email,
        email=email,
        name=name,
        dp="https://picsum.photos/seed/yogeshdevaggarwal/200/200",
        password="12345678",
    )

    reminder = Reminder(
        _id="reminder1",
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
        _id="notification1",
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
        _id=f"digest0",
        user_id=user.id,
        date_created=int(datetime.now().timestamp() * 1000),
        date_updated=int(datetime.now().timestamp() * 1000),
        title="Test emails",
        description="This digest contains test emails from any source",
    )
    digest.create()
    for i in range(1, 4):
        digest = Digest(
            _id=f"digest{i}",
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
            _id=f"thread{i}",
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
                is_sent=False,
                is_spam=False,
            ),
        )
        thread.create()

    for i in range(1, 20):
        message = Message(
            _id=f"message{i}",
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
            reminders=MessageReminders(
                follow_up=[],
                forgetting=[],
                snoozed=[],
            ),
            summary="Sample summary",
            priorities=["high"],
            categories=[
                random.choice(["Primary", "Social", "Promotions", "Updates", "Forums"])
            ],
            labels=[f"label{i}"],
            digests=[f"digest{random.choice([1, 2, 3])}"],
            embedding=[0.0] * 384,  # Default empty embedding
            keywords=["sample", "email", f"keyword{i}"],
            unsubscribe_link=None,
        )
        message.create()

    data = Data(
        _id="data1",
        user_id=user.id,
        date_created=int(datetime.now().timestamp() * 1000),
        type=DataType.EMAIL_RECEIVED,
        data={"key": "value"},
    )
    data.create()


async def _setup_users():
    users = [
        ("Yogesh Aggarwal", "yogeshdevaggarwal@gmail.com"),
    ]

    jobs = map(lambda x: _setup_user(*x), users)
    await asyncio.gather(*jobs)


def main():
    print("Starting database seeding...")
    asyncio.run(_setup_users())
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    main()

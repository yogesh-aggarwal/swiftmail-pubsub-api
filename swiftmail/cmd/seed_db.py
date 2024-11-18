import asyncio
import random
import time
from datetime import datetime
from bson import ObjectId

from swiftmail.api.models.data import Data, DataType
from swiftmail.api.models.digest import Digest
from swiftmail.api.models.message import Message, MessageEmailData, MessageReminders
from swiftmail.api.models.notification import Notification, NotificationStatus
from swiftmail.api.models.reminder import Reminder, ReminderState, ReminderType
from swiftmail.api.models.thread import Thread, ThreadFlags
from swiftmail.api.models.user import User
from swiftmail.core.mongodb import db


async def create_reminder(user_id: str, message_id: str, thread_id: str) -> None:
    reminder = Reminder(
        _id=ObjectId(),
        user_id=user_id,
        date_created=int(datetime.now().timestamp() * 1000),
        date_updated=int(datetime.now().timestamp() * 1000),
        scheduled_at=int(datetime.now().timestamp() + 3600),  # 1 hour later
        time_zone="UTC",
        message_id=message_id,
        thread_id=thread_id,
        type=ReminderType.FOLLOW_UP,
        state=ReminderState.NOT_STARTED,
    )
    reminder.create()


async def create_notification(user_id: str) -> None:
    notification = Notification(
        _id=ObjectId(),
        user_id=user_id,
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


async def create_digests(user_id: str) -> list[str]:
    digest_ids = []

    # Create main digest
    digest = Digest(
        _id=ObjectId(),
        user_id=user_id,
        date_created=int(datetime.now().timestamp() * 1000),
        date_updated=int(datetime.now().timestamp() * 1000),
        title="Test emails",
        description="This digest contains test emails from any source",
    )
    digest.create()

    # Create additional digests
    titles = ["College placements", "Funding updates", "SaaS updates"]
    for title in titles:
        digest_id = ObjectId()
        digest_ids.append(digest_id)
        digest = Digest(
            _id=digest_id,
            user_id=user_id,
            date_created=int(datetime.now().timestamp() * 1000),
            date_updated=int(datetime.now().timestamp() * 1000),
            title=title,
            description="This is a sample digest",
        )
        digest.create()

    return digest_ids


async def create_threads(user_id: str) -> list[str]:
    thread_ids = []
    for i in range(1, 20):
        thread = Thread(
            user_id=user_id,
            date_created=int(datetime.now().timestamp() * 1000),
            date_updated=int(datetime.now().timestamp() * 1000),
            title=f"Sample Thread {i}",
            description=f"This is a sample thread {i}",
            summary="Sample summary",
            thread_id=str(ObjectId()),
            priority=random.choice(["low", "medium", "high"]),
            categories=[
                random.choice(["Primary", "Social", "Promotions", "Updates", "Forums"])
            ],
            labels=[],
            digests=[],
            flags=ThreadFlags(
                is_muted=random.choice([True, False]),
                is_starred=random.choice([True, False]),
                is_trash=random.choice([True, False]),
                is_archived=random.choice([True, False]),
                is_read=random.choice([True, False]),
                is_sent=random.choice([True, False]),
                is_spam=random.choice([True, False]),
            ),
        )
        thread_ids.append(str(thread.id))
        thread.create()
    return thread_ids


async def create_messages(
    user_id: str, thread_ids: list[str], digest_ids: list[str]
) -> None:
    for i in range(1, 20):
        message_id = ObjectId()
        message = Message(
            _id=message_id,
            user_id=user_id,
            date_created=int(datetime.now().timestamp() * 1000),
            date_updated=int(datetime.now().timestamp() * 1000),
            email_data=MessageEmailData(
                subject=f"Sample Subject {i}",
                html_content="<p>This is a sample email content</p>",
                message_id=str(message_id),
                thread_id=random.choice(thread_ids),
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
            embedding=[0.0] * 384,  # Default empty embedding
            keywords=["sample", "email", f"keyword{i}"],
            unsubscribe_link=None,
        )
        message.create()

        thread = Thread.get_by_id(thread_ids[(i % 2) + 1])
        if thread:
            thread.priority = "high"
            thread.categories = [
                random.choice(["Primary", "Social", "Promotions", "Updates", "Forums"])
            ]
            thread.labels = [f"label{i}"]
            thread.digests = [random.choice(digest_ids)]
            thread.save()


async def create_data(user_id: str) -> None:
    data = Data(
        _id=ObjectId(),
        user_id=user_id,
        date_created=int(datetime.now().timestamp() * 1000),
        type=DataType.EMAIL_RECEIVED,
        data={"key": "value"},
    )
    data.create()


async def setup_user(name: str, email: str):
    start_time = time.time()
    print(f"\nSetting up user: {name} ({email})")

    # Create user
    user_start = time.time()
    user = User.create(
        email=email,
        name=name,
        dp="https://picsum.photos/seed/yogeshdevaggarwal/200/200",
        password="12345678",
    )
    print(f"✓ Created user in {time.time() - user_start:.2f}s")

    # Create digests and threads
    digest_start = time.time()
    digest_ids = await create_digests(str(user.id))
    print(f"✓ Created digests in {time.time() - digest_start:.2f}s")

    thread_start = time.time()
    thread_ids = await create_threads(str(user.id))
    print(f"✓ Created threads in {time.time() - thread_start:.2f}s")

    # Create remaining entities in parallel
    parallel_start = time.time()
    await asyncio.gather(
        # create_reminder(str(user.id), str(message_id), str(thread_id)),
        create_notification(str(user.id)),
        create_messages(str(user.id), thread_ids, digest_ids),
        create_data(str(user.id)),
    )
    print(f"✓ Created remaining entities in {time.time() - parallel_start:.2f}s")

    print(f"✓ Total setup time for {name}: {time.time() - start_time:.2f}s")


async def setup_users():
    users = [
        ("Yogesh Aggarwal", "yogeshdevaggarwal@gmail.com"),
    ]

    start_time = time.time()
    jobs = map(lambda x: setup_user(*x), users)
    await asyncio.gather(*jobs)
    print(f"\nTotal time for all users: {time.time() - start_time:.2f}s")


def main():
    start_time = time.time()
    print("Starting database seeding...")

    # Delete all collections
    collections = db.list_collection_names()
    drop_start = time.time()
    for collection in collections:
        db.drop_collection(collection)
    print(f"✓ Dropped all collections in {time.time() - drop_start:.2f}s")

    # Run setup
    asyncio.run(setup_users())
    print(f"\nTotal execution time: {time.time() - start_time:.2f}s")
    print("Database seeding completed successfully!")


if __name__ == "__main__":
    main()

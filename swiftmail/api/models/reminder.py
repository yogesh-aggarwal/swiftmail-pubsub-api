from pydantic import BaseModel
from enum import Enum
from swiftmail.core.firebase import REMINDERS_COLLECTION


class ReminderType(str, Enum):
    FOLLOW_UP = "follow-up"
    FORGETTING = "forgetting"
    SNOOZED = "snoozed"


class ReminderState(str, Enum):
    NOT_STARTED = "not_started"
    IN_QUEUE = "in_queue"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Reminder(BaseModel):
    id: str
    user_id: str
    date_created: int
    date_updated: int

    scheduled_at: int
    time_zone: str

    message_id: str
    thread_id: str

    type: ReminderType
    state: ReminderState

    @staticmethod
    def get_by_id(reminder_id: str) -> "Reminder | None":
        reminder = REMINDERS_COLLECTION.document(reminder_id).get()
        if reminder.exists:
            return Reminder(**reminder.to_dict())  # type:ignore
        return None

    def save(self):
        REMINDERS_COLLECTION.document(self.id).set(self.model_dump())

    def create(self):
        self.save()

    def update_type(self, type: ReminderType):
        self.type = type
        self.save()

    def update_state(self, state: ReminderState):
        self.state = state
        self.save()

    def update_scheduled_at(self, scheduled_at: int):
        self.scheduled_at = scheduled_at
        self.save()

    def update_time_zone(self, time_zone: str):
        self.time_zone = time_zone
        self.save()

from enum import Enum
from swiftmail.core.utils import generate_id
from typing import Optional
from swiftmail.core.mongodb import REMINDERS
from .base import MongoModel
from pydantic import Field


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


class Reminder(MongoModel):
    user_id: str = Field(..., alias="user_id")
    date_created: int = Field(..., alias="date_created")
    date_updated: int = Field(..., alias="date_updated")
    scheduled_at: int = Field(..., alias="scheduled_at")
    time_zone: str = Field(..., alias="time_zone")
    message_id: str = Field(..., alias="message_id")
    thread_id: str = Field(..., alias="thread_id")
    type: ReminderType = Field(..., alias="type")
    state: ReminderState = Field(..., alias="state")

    @staticmethod
    def get_by_id(reminder_id: str) -> Optional["Reminder"]:
        reminder = REMINDERS.find_one({"id": reminder_id})
        return Reminder.from_mongo(reminder) if reminder else None

    def create(self):
        self._save(REMINDERS)

    def update_type(self, type: ReminderType):
        self.type = type
        self._save(REMINDERS)

    def update_state(self, state: ReminderState):
        self.state = state
        self._save(REMINDERS)

    def update_scheduled_at(self, scheduled_at: int):
        self.scheduled_at = scheduled_at
        self._save(REMINDERS)

    def update_time_zone(self, time_zone: str):
        self.time_zone = time_zone
        self._save(REMINDERS)

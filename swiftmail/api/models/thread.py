from typing import List
from pydantic import BaseModel, Field

from .base import MongoModel

from swiftmail.core.mongodb import THREADS, MESSAGES
from swiftmail.api.models.message import Message


class ThreadFlags(BaseModel):
    is_muted: bool = Field(..., alias="is_muted")
    is_read: bool = Field(..., alias="is_read")
    is_starred: bool = Field(..., alias="is_starred")
    is_archived: bool = Field(..., alias="is_archived")

    is_spam: bool = Field(..., alias="is_spam")
    is_trash: bool = Field(..., alias="is_trash")
    is_sent: bool = Field(..., alias="is_sent")


class Thread(MongoModel):
    user_id: str = Field(..., alias="user_id")
    date_updated: int = Field(..., alias="date_updated")
    date_created: int = Field(..., alias="date_created")

    title: str = Field(..., alias="title")
    description: str = Field(..., alias="description")

    summary: str = Field(..., alias="summary")
    thread_id: str = Field(..., alias="thread_id")

    flags: ThreadFlags = Field(..., alias="flags")

    priority: str = Field(alias="priority")
    categories: List[str] = Field(default_factory=list, alias="categories")
    labels: List[str] = Field(default_factory=list, alias="labels")
    digests: List[str] = Field(default_factory=list, alias="digests")

    @staticmethod
    def get_by_id(thread_id: str) -> "Thread | None":
        """
        Fetches a thread by its ID.

        Args:
            thread_id (str): The ID of the thread.

        Returns:
            Thread | None: The Thread instance if found, else None.
        """
        thread_doc = THREADS.find_one({"id": thread_id})
        if thread_doc:
            return Thread.from_mongo(thread_doc)
        return None

    @staticmethod
    def get_messages_by_thread(
        thread_id: str, page: int, page_size: int = 10
    ) -> list["Message"]:
        """
        Fetches messages associated with a specific thread_id, sorted by date_created and paginated.

        Args:
            thread_id (str): The ID of the thread.
            page (int): The page number to retrieve.
            page_size (int, optional): Number of messages per page. Defaults to 10.

        Returns:
            list[Message]: A list of Message instances.
        """
        skip = (page - 1) * page_size
        messages = (
            MESSAGES.find({"thread_id": thread_id})
            .sort("date_created", 1)
            .skip(skip)
            .limit(page_size)
        )

        results = []
        for msg in messages:
            result = Message.from_mongo(msg)
            if result:
                results.append(result)

        return results

    def save(self):
        self._save(THREADS)

    def create(self):
        """Create a new thread in the database"""
        self.save()

    def mark_as_read(self):
        """Mark the thread as read and save"""
        self.flags.is_read = True
        self.save()

    def mark_as_unread(self):
        """Mark the thread as unread and save"""
        self.flags.is_read = False
        self.save()

    def toggle_starred(self):
        """Toggle starred status and save"""
        self.flags.is_starred = not self.flags.is_starred
        self.save()

    def mark_as_archived(self):
        """Archive the thread and save"""
        self.flags.is_archived = True
        self.save()

    def mark_as_unarchived(self):
        """Unarchive the thread and save"""
        self.flags.is_archived = False
        self.save()

    def mark_as_spam(self):
        """Mark as spam and save"""
        self.flags.is_spam = True
        self.flags.is_trash = False
        self.save()

    def mark_as_not_spam(self):
        """Mark as not spam and save"""
        self.flags.is_spam = False
        self.save()

    def mark_as_trash(self):
        """Move to trash and save"""
        self.flags.is_trash = True
        self.flags.is_spam = False
        self.save()

    def restore_from_trash(self):
        """Restore from trash and save"""
        self.flags.is_trash = False
        self.save()

    def mark_as_muted(self):
        """Mark as muted and save"""
        self.flags.is_muted = True
        self.save()

    def mark_as_unmuted(self):
        """Mark as unmuted and save"""
        self.flags.is_muted = False
        self.save()

    def mark_as_sent(self):
        """Mark as sent and save"""
        self.flags.is_sent = True
        self.save()

    def add_category(self, category: str):
        """Add a category if it doesn't exist"""
        if category not in self.categories:
            self.categories.append(category)
            self.save()

    def remove_category(self, category: str):
        """Remove a category if it exists"""
        if category in self.categories:
            self.categories.remove(category)
            self.save()

    def add_label(self, label: str):
        """Add a label if it doesn't exist"""
        if label not in self.labels:
            self.labels.append(label)
            self.save()

    def remove_label(self, label: str):
        """Remove a label if it exists"""
        if label in self.labels:
            self.labels.remove(label)
            self.save()

    def add_digest(self, digest_id: str):
        """Add a digest reference if it doesn't exist"""
        if digest_id not in self.digests:
            self.digests.append(digest_id)
            self.save()

    def remove_digest(self, digest_id: str):
        """Remove a digest reference if it exists"""
        if digest_id in self.digests:
            self.digests.remove(digest_id)
            self.save()

    def clear_categories(self):
        """Remove all categories"""
        self.categories = []
        self.save()

    def clear_labels(self):
        """Remove all labels"""
        self.labels = []
        self.save()

    def clear_digests(self):
        """Remove all digest references"""
        self.digests = []
        self.save()

    def set_priority(self, priority: str):
        """Set the thread priority"""
        self.priority = priority
        self.save()

    def set_categories(self, categories: List[str]):
        """Set the entire categories list"""
        self.categories = list(set(categories))  # Remove duplicates
        self.save()

    def set_labels(self, labels: List[str]):
        """Set the entire labels list"""
        self.labels = list(set(labels))  # Remove duplicates
        self.save()

    def set_digests(self, digests: List[str]):
        """Set the entire digests list"""
        self.digests = list(set(digests))  # Remove duplicates
        self.save()

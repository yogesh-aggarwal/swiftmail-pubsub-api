from pymongo import MongoClient
from pymongo.database import Database

from swiftmail.core.constants import MONGODB_URI

client = MongoClient(MONGODB_URI)
db: Database = client["swiftmail"]

# Collections
USERS = db["users"]
MESSAGES = db["messages"]
THREADS = db["threads"]
REMINDERS = db["reminders"]
NOTIFICATIONS = db["notifications"]
DIGESTS = db["digests"]
DATA = db["data"]

# Create indexes
USERS.create_index("email", unique=True)
MESSAGES.create_index("user_id")
MESSAGES.create_index("thread_id")
THREADS.create_index("user_id")
REMINDERS.create_index("user_id")
NOTIFICATIONS.create_index("user_id")
DIGESTS.create_index("user_id")
DATA.create_index("user_id")

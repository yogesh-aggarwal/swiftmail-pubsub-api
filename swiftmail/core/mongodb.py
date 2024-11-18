from pymongo import MongoClient
from pymongo.database import Database

client = MongoClient("mongodb://localhost:27017")
db: Database = client["swiftmail"]

# Collections
users = db["users"]
messages = db["messages"]
threads = db["threads"]
reminders = db["reminders"]
notifications = db["notifications"]
digests = db["digests"]
dashboards = db["dashboards"]
data = db["data"]

# Create indexes
users.create_index("email", unique=True)
messages.create_index("user_id")
messages.create_index("thread_id")
threads.create_index("user_id")
reminders.create_index("user_id")
notifications.create_index("user_id")
digests.create_index("user_id")
dashboards.create_index("user_id")
data.create_index("user_id") 
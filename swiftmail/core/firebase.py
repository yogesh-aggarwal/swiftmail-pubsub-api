import firebase_admin
from firebase_admin import auth, credentials, firestore

from .constants import GCP_CREDENTIALS_FILE

cred = credentials.Certificate(GCP_CREDENTIALS_FILE)
firebase_admin.initialize_app(cred)

db = firestore.client()
auth = auth

DASHBOARDS_COLLECTION = db.collection("dashboards")
DATA_COLLECTION = db.collection("data")
DIGESTS_COLLECTION = db.collection("digests")
MESSAGES_COLLECTION = db.collection("messages")
NOTIFICATIONS_COLLECTION = db.collection("notifications")
THREADS_COLLECTION = db.collection("threads")
USERS_COLLECTION = db.collection("users")

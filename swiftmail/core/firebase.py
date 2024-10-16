import firebase_admin
from firebase_admin import auth, credentials, firestore

from .constants import GCP_CREDENTIALS_FILE

cred = credentials.Certificate(GCP_CREDENTIALS_FILE)
firebase_admin.initialize_app(cred)

db = firestore.client()
auth = auth

USERS_COLLECTION = db.collection("users")

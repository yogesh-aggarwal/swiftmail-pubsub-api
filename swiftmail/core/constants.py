import os
from typing import Any

from dotenv import load_dotenv

load_dotenv()


def get_from_env_or_raise(key: str, default: Any | None = None) -> str:
    value = os.getenv(key, default)
    assert value is not None, f"Please set the {key} environment variable."
    return value


# ---------------------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------------------

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "*.vercel.app",
    "*.web.app",
]

POLL_INTERVAL_IN_SECONDS = 10

# ---------------------------------------------------------------------------------------
# Check for necessary files' existence
# ---------------------------------------------------------------------------------------

# GCP credentials file
GCP_CREDENTIALS_FILE = get_from_env_or_raise("GCP_CREDENTIALS_FILE")
assert os.path.exists(GCP_CREDENTIALS_FILE), f"{GCP_CREDENTIALS_FILE} does not exist."

# ---------------------------------------------------------------------------------------
# General
# ---------------------------------------------------------------------------------------

PORT = int(get_from_env_or_raise("PORT", 3000))

# ---------------------------------------------------------------------------------------
# Gen AI
# ---------------------------------------------------------------------------------------

OPENAI_API_KEY = get_from_env_or_raise("OPENAI_API_KEY")
HF_API_KEY = get_from_env_or_raise("HF_API_KEY")

# ---------------------------------------------------------------------------------------
# URIS
# ---------------------------------------------------------------------------------------

REDIS_URI = get_from_env_or_raise("REDIS_URI")

# ---------------------------------------------------------------------------------------
# Google
# ---------------------------------------------------------------------------------------

GOOGLE_OAUTH_CLIENT_ID = get_from_env_or_raise("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET = get_from_env_or_raise("GOOGLE_OAUTH_CLIENT_SECRET")
GOOGLE_OAUTH_REDIRECT_URI = get_from_env_or_raise("GOOGLE_OAUTH_REDIRECT_URI")

# ---------------------------------------------------------------------------------------
# MongoDB
# ---------------------------------------------------------------------------------------

MONGODB_URI = get_from_env_or_raise("MONGODB_URI")

# ---------------------------------------------------------------------------------------

from pydantic import BaseModel
from swiftmail.api.models.message import MessageEmailData
from swiftmail.api.models.user import User


# Job Input Models
class ProcessEmailJobData(BaseModel):
    email: MessageEmailData
    user: User


# Processing Result Models
class EmailClassificationResult(BaseModel):
    spam: bool
    priority: str
    labels: list[str]
    categories: list[str]
    unsubscribe_link: str | None
    keywords: list[str]


# Email Digest Result Models
class EmailDigestResult(BaseModel):
    digests: list[str]


# Email Summary Result Models
class EmailSummaryResult(BaseModel):
    summary: str


# Email Embedding Result Models
class EmailEmbeddingResult(BaseModel):
    embedding: list[float]

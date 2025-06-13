from pydantic import BaseModel, Field
from uuid import UUID

class QueryRequest(BaseModel):
    user_id: str
    query: str

class ProductDocument(BaseModel):
    id: UUID
    content: str
    embeddings: list[float] = Field(None, exclude=True)


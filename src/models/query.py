from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    user_id: str
    query: str


class ProductDocument(BaseModel):
    id: int
    content: str
    embeddings: list[float] = Field(None, exclude=True)

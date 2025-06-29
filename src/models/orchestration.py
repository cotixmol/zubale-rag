from pydantic import BaseModel, Field
from typing import List
from src.models.query import ProductDocument


class AgentState(BaseModel):
    user_id: str = ""
    query: str = ""
    documents: List[ProductDocument] = Field(default_factory=list)
    response: str = ""

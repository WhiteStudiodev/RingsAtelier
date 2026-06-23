from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LeadCreate(BaseModel):
    name: str = Field(..., min_length=2)
    method: str = Field(..., pattern="^(tg|max|vk|phone)$")
    contact: str = Field(..., min_length=1)
    message: Optional[str] = None


class LeadOut(LeadCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

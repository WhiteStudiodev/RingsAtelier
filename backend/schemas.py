import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ValidationInfo, field_validator


PHONE_RE = re.compile(r'^(?:\+7|8)?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$')


class LeadCreate(BaseModel):
    name: str
    method: str
    contact: str
    message: Optional[str] = None

    @field_validator('contact')
    @classmethod
    def validate_contact(cls, v: str, info: ValidationInfo) -> str:
        data = info.data or {}
        if data.get('method') == 'vk':
            if 'vk.com/' not in v and len(v.strip()) < 3:
                raise ValueError('Введите ссылку или ID')
        else:
            if not PHONE_RE.match(v.strip()):
                raise ValueError('Неверный формат номера')
        return v


class LeadOut(LeadCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

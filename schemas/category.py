from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class CategorySchema(BaseModel):
    category_name: str
    parent_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class CategorySchemaUpdate(BaseModel):
    category_name: Optional[str] = None
    parent_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


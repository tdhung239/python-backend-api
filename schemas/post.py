from pydantic import BaseModel, fields
from typing import Optional
from pydantic.schema import datetime


class PostSchema(BaseModel):
    category_id: int
    author_id: int
    post_title: str
    post_image: str
    post_detail_short: str
    post_detail: str
    post_view: Optional[int] = None
    post_hot: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


class PostSchemaUpdate(BaseModel):
    category_id: Optional[int] = None
    author_id: Optional[int] = None
    post_title: Optional[str] = None
    post_image: Optional[str] = None
    post_detail_short: Optional[str] = None
    post_detail: Optional[str] = None
    post_view: Optional[int] = None
    post_hot: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

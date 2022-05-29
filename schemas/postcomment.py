from pydantic import BaseModel


class CreateCommentSchema(BaseModel):
    parent_id: int
    content: str


class UpdateCommentSchema(BaseModel):
    content: str

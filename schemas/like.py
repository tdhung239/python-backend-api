from pydantic import BaseModel


class LikeSchema(BaseModel):
    id: int
    post_id: int
    like_count: int
    like_user: str

from pydantic import BaseModel
from typing import Optional


class ProfileSchemaUpdateImage(BaseModel):
    avatar: Optional[str] = None

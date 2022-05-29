from pydantic import BaseModel, validator
from utils.confession import validate_content_null
from fastapi import HTTPException
from http import HTTPStatus


class HyboxSchema(BaseModel):
    content: str

    @validator('content')
    def validate_content(cls, v):
        if validate_content_null(v):
            return v
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Please Insert Something to HyBox")


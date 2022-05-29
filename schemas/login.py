from http import HTTPStatus

from pydantic import BaseModel, ValidationError, validator
from typing import Optional
from common.auth import validate_email
from fastapi import HTTPException

class LoginSchema(BaseModel):
    email: str
    password: str

    @validator('email')
    def validate_email(cls, v):
        if not validate_email(v):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Enter invalidate email")
        return v


class TokenData(BaseModel):
    username: Optional[str] = None


class EmailSchema(BaseModel):
    email: str

    @validator('email')
    def validate_email(cls, v):
        if not validate_email(v):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Enter invalidate email")
        return v

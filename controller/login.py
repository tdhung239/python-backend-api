from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db_session
from services.login import LoginService
from schemas.login import LoginSchema, EmailSchema
from common.auth import verify
from common.reponse import make_bad_request_response, make_oke_request_response

router = APIRouter(tags=['Authentication'])


@router.post("/login")
async def login(data: LoginSchema, db_session: Session = Depends(get_db_session)):
    login_service = LoginService(db_session)

    try:
        result = await login_service.login(data)
        return make_oke_request_response(result)
    except Exception as ex:
        return make_bad_request_response(ex)


@router.get("/logout", dependencies=[Depends(verify)])
async def logout(db_session: Session = Depends(get_db_session), auth_user=Depends(verify)):
    login_service = LoginService(db_session)

    try:
        result = await login_service.logout(auth_user)
        return make_oke_request_response(result)
    except Exception as ex:
        return make_bad_request_response(ex)


@router.post("/forgot_password")
async def forgot_password(data: EmailSchema, db_session: Session = Depends(get_db_session)):
    login_service = LoginService(db_session)

    try:
        result = await login_service.forgot_password(data)
        return make_oke_request_response(result)
    except Exception as ex:
        return make_bad_request_response(ex)

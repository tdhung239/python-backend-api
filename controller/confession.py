from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db_session
from services.confession import ConfessionService
from common.auth import verify
from common.reponse import make_oke_request_response, make_bad_request_response
from schemas.confession import HyboxSchema

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/confessions")
async def confession_list(db_session: Session = Depends(get_db_session)):
    confession_service = ConfessionService(db_session)
    result = await confession_service.get_confessions()
    return make_oke_request_response({"result": result})


@router.post('/hy_box')
async def create_hy_box(hy_box: HyboxSchema, db_session: Session = Depends(get_db_session),auth_user=Depends(verify)):
    confession_service = ConfessionService(db_session)

    try:
        await confession_service.create_confess(hy_box,auth_user)
        return make_oke_request_response({"result": "Hy_Box Created Successful"})
    except Exception as error:
        return make_bad_request_response(error)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common.auth import verify
from config.database import get_db_session
from services.user import UserService

from common.reponse import make_oke_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/users")
async def profile_list(db_session: Session = Depends(get_db_session)):
    profile_service = UserService(db_session)
    result = await profile_service.get_users()
    return make_oke_request_response({"result": result})

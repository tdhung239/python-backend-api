from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db_session
from services.role import RoleService
from common.auth import verify
from common.reponse import make_oke_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/roles")
async def profile_list(db_session: Session = Depends(get_db_session)):
    profile_service = RoleService(db_session)
    result = await profile_service.get_roles()
    return make_oke_request_response({"result": result})

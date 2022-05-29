from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db_session
from services.bannershow import BannershowService
from common.auth import verify
from common.reponse import make_oke_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/bannershows")
async def profile_list(db_session: Session = Depends(get_db_session)):
    profile_service = BannershowService(db_session)
    result = await profile_service.get_bannershows()
    return make_oke_request_response({"result": result})

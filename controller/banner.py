from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from common.auth import verify
from config.database import get_db_session
from services.banner import BannerService
from common.reponse import make_oke_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/banners")
async def profile_list(db_session: Session = Depends(get_db_session)):
    profile_service = BannerService(db_session)
    result = await profile_service.get_banners()
    return make_oke_request_response({"result": result})

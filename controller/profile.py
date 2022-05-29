from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from config.database import get_db_session
from common.auth import verify
from services.profile import ProfileService
from schemas.profile import ProfileSchemaUpdateImage
from common.reponse import make_bad_request_response, make_oke_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/profiles")
async def profile_list(db_session: Session = Depends(get_db_session), auth_user=Depends(verify)):
    profile_service = ProfileService(db_session)

    try:
        result = await profile_service.get_profile(auth_user)
        return make_oke_request_response({"result": result})
    except Exception as ex:
        return make_bad_request_response(ex)


@router.put("/profile")
async def update_image_profile(data: ProfileSchemaUpdateImage, db_session: Session = Depends(get_db_session), auth_user=Depends(verify)):
    profile_service = ProfileService(db_session)

    try:
        result = await profile_service.update_image_profile(auth_user, data)
        return make_oke_request_response({"result": result})
    except Exception as ex:
        return make_bad_request_response(ex)


@router.put("/profile2")
async def update_image_profile2(db_session: Session = Depends(get_db_session), auth_user=Depends(verify), file: UploadFile = File(...)):
    profile_service = ProfileService(db_session)

    try:
        result = await profile_service.update_image_profile2(auth_user, file)
        return make_oke_request_response({"result": result})
    except Exception as ex:
        return make_bad_request_response(ex)

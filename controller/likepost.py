from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db_session
from services.likepost import LikePostService
from common.auth import verify
from common.reponse import make_oke_request_response, make_bad_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/posts/{id_post}/likes")
async def like_list(id_post: int, db_session: Session = Depends(get_db_session)):
    like_post_service = LikePostService(db_session)

    try:
        result = await like_post_service.get_like_posts(id_post)
        return make_oke_request_response(result)
    except Exception as ex:
        return make_bad_request_response(ex)


@router.post("/posts/{id_post}/likes")
async def create_like(id_post: int, db_session: Session = Depends(get_db_session), auth_user=Depends(verify)):
    like_post_service = LikePostService(db_session)

    try:
        await like_post_service.create_like(auth_user, id_post)
        return make_oke_request_response({"result": "successfully"})
    except Exception as ex:
        return make_bad_request_response(ex)

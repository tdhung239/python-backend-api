from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from common.auth import verify
from common.reponse import make_oke_request_response, make_bad_request_response
from schemas.postcomment import CreateCommentSchema, UpdateCommentSchema
from config.database import get_db_session
from services.potscomment import PostCommentService

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/post/{id_post}/comments")
async def get_comment(id_post: int, page=1, limit=0, db_session: Session = Depends(get_db_session)):
    get_post_comment = PostCommentService(db_session)
    try:
        result = await get_post_comment.get_post_comments(id_post, int(page), int(limit))

        return make_oke_request_response({
            "result": result
        })
    except Exception as ex:
        return make_bad_request_response(ex)


@router.post("/post/{id_post}/comments")
async def create_comment(data: CreateCommentSchema, id_post: int,
                         db_session: Session = Depends(get_db_session), auth_user=Depends(verify)):
    create_post_comment = PostCommentService(db_session)

    try:
        result = await create_post_comment.create_post_comments(id_post, data, auth_user)
        return make_oke_request_response({
            "result": result
        })
    except Exception as ex:
        return make_bad_request_response(ex)


@router.put("/post/{id_post}/comments/{id_cmt}")
async def update_comment(id_post: int, id_cmt: int, data: UpdateCommentSchema,
                         db_session: Session = Depends(get_db_session), auth_user=Depends(verify)):
    cmt_service = PostCommentService(db_session)

    try:
        result = await cmt_service.update_post_comments(id_post, id_cmt, data, auth_user)
        return make_oke_request_response({
            "result": result
        })
    except Exception as ex:
        return make_bad_request_response(ex)


@router.delete("/delete/{id_cmt}")
async def delete_comment(id_cmt: int, db_session: Session = Depends(get_db_session),
                         auth_user=Depends(verify)):
    cmt_service = PostCommentService(db_session)

    try:
        result = await cmt_service.delete_post_comments(id_cmt, auth_user)
        return make_oke_request_response({
            "result": result
        })
    except Exception as ex:
        return make_bad_request_response(ex)

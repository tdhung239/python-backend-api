from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db_session
from services.post import PostService
from schemas.post import PostSchema, PostSchemaUpdate
from common.auth import verify
from common.reponse import make_oke_request_response, make_bad_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/posts")
async def get_list_post(id_category=None, sort_by=None, page=0, limit=0, db_session: Session = Depends(get_db_session)):
    post_service = PostService(db_session)

    try:
        if id_category is not None:
            if int(limit) > 0 and int(page) > 0:
                result = await post_service.get_post_limit(int(id_category), sort_by, int(page), int(limit))
            else:
                result = await post_service.get_posts(int(id_category))
        else:
            raise ValueError("Value invalid! Not found data")
    except Exception as ex:
        return make_bad_request_response(ex)
    return make_oke_request_response(result)


@router.post("/posts")
async def create_post(data: PostSchema, db_session: Session = Depends(get_db_session)):
    post_service = PostService(db_session)
    await post_service.create_post(data)
    return make_oke_request_response({"result": "create successfully"})


@router.put("/posts/{post_id}")
async def update_post(post_id: int, data: PostSchemaUpdate, db_session: Session = Depends(get_db_session)):
    post_service = PostService(db_session)

    try:
        await post_service.update_post(post_id, data)
        return make_oke_request_response({"result": "update successfully"})
    except Exception as ex:
        return make_bad_request_response(ex)


@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db_session: Session = Depends(get_db_session)):
    post_service = PostService(db_session)
    await post_service.delete_post(post_id)
    return make_oke_request_response({"result": "delete successfully"})


@router.get("/post/{id}")
async def post_id(id: int, db_session: Session = Depends(get_db_session)):
    try:
        profile_service = PostService(db_session)
        result = await profile_service.get_post_by_id(id)
        return make_oke_request_response({"result": result})
    except Exception as error:
        return make_bad_request_response(error)

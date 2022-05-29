from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db_session
from services.category import CategoryService
from schemas.category import CategorySchema, CategorySchemaUpdate
from common.auth import verify
from common.reponse import make_bad_request_response, make_oke_request_response

router = APIRouter(dependencies=[Depends(verify)])


@router.get("/categories")
async def get_category_home(db_session: Session = Depends(get_db_session)):
    category_service = CategoryService(db_session)
    result = await category_service.get_categorys_home()
    return make_oke_request_response({"result": result})


@router.post("/categories")
async def create_category(data: CategorySchema, db_session: Session = Depends(get_db_session)):
    category_service = CategoryService(db_session)

    try:
        await category_service.create_category(data)
        return make_oke_request_response({"result": "create successfully"})
    except Exception as ex:
        return make_bad_request_response(ex)


@router.put("/categories/:id_category")
async def update_category(id_category: int, data: CategorySchemaUpdate, db_session: Session = Depends(get_db_session)):
    category_service = CategoryService(db_session)

    try:
        await category_service.update_category(id_category, data)
        return make_oke_request_response({"result": "update successfully"})
    except Exception as ex:
        return make_bad_request_response(ex)


@router.get("/categories/{parent_id}")
async def get_list_subcategory(parent_id: int, db_session: Session = Depends(get_db_session)):
    category_service = CategoryService(db_session)

    try:
        result = await category_service.get_categorys(parent_id)
        return make_oke_request_response({"data": result})
    except Exception as ex:
        return make_bad_request_response(ex)
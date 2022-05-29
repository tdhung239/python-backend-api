from sqlalchemy import null
from sqlalchemy.orm import Session
from models.category import Category
from schemas.category import CategorySchema, CategorySchemaUpdate


class CategoryService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_categorys(self, parent_id: int):
        try:
            result = self.db_session.query(Category)\
                .filter(Category.deleted_at == null(), Category.parent_id == parent_id)
            rs = [{"id": item.id, "name": item.category_name, "parent_id": item.parent_id} for item in result]
            return rs
        except Exception as ex:
            raise ex

    async def get_categorys_home(self):
        try:
            result = self.db_session.query(Category).filter(Category.parent_id == null(), Category.deleted_at == null())
            rs = [{"id": item.id, "name": item.category_name, "parent_id": item.parent_id} for item in result]
            return rs
        except Exception as ex:
            raise ex

    async def get_categorys_parentid(self, parent_id: int):
        try:
            query_a = self.db_session.query(Category). \
                filter(Category.id == parent_id, Category.deleted_at == null()) \
                .cte('cte', recursive=True)
            query_b = self.db_session.query(Category).join(query_a, Category.parent_id == query_a.c.id)
            recursive_q = query_a.union(query_b)
            result = self.db_session.query(recursive_q).filter(recursive_q.c.id != parent_id).all()
            rs = [{"id": item.id, "name": item.category_name} for item in result]
            return rs
        except Exception as ex:
            raise ex

    async def create_category(self, data: CategorySchema):
        try:
            catogery = Category(category_name=data.category_name, parent_id=data.parent_id, created_at=data.created_at,
                                updated_at=data.updated_at, deleted_at=data.deleted_at)
            self.db_session.add(catogery)
            self.db_session.flush()
        except Exception as ex:
            raise ex

    async def update_category(self, id_category: int, data: CategorySchemaUpdate):
        try:
            category_update = self.db_session.query(Category).filter(Category.id == id_category)
            if not category_update:
                raise ValueError(f"catogery with {id_category} not exist")
            else:
                category_temp = {}
                for key, value in dict(data).items():
                    if value is not None:
                        category_temp.update({key: value})
                category_update.update(category_temp)
                self.db_session.flush()
        except Exception as ex:
            raise ex

    async def get_one_category(self, category_id: int):
        try:
            result = self.db_session.query(Category). \
                filter(Category.id == category_id, Category.deleted_at == null()).first()
            if not result:
                raise ValueError(f"category with {id} not exist")
            return {"id": result.id, "name": result.category_name, "parent_id": result.parent_id}
        except Exception as ex:
            raise ex
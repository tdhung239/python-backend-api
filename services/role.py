# from traceback import print_stack

from sqlalchemy.orm import Session

from models.role import Role


class RoleService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_roles(self):
        try:
            result = self.db_session.query(Role).all()
            return result
        except Exception as ex:
            raise ex




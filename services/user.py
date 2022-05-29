# from traceback import print_stack

from sqlalchemy.orm import Session

from models.user import User


class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_users(self):
        try:
            result = self.db_session.query(User).all()
            return result
        except Exception as ex:
            raise ex


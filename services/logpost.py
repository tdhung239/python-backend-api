# from traceback import print_stack

from sqlalchemy.orm import Session

from models.logpost import Logpost


class LogpostService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_logposts(self):
        try:
            result = self.db_session.query(Logpost).all()
            return result
        except Exception as ex:
            raise ex


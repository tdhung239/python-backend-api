# from traceback import print_stack

from sqlalchemy.orm import Session

from models.bannershow import Bannershow


class BannershowService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_bannershows(self):
        try:
            result = self.db_session.query(Bannershow).all()
            return result
        except Exception as ex:
            raise ex


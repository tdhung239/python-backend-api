# from traceback import print_stack

from sqlalchemy.orm import Session

from models.banner import Banner


class BannerService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_banners(self):
        try:
            result = self.db_session.query(Banner).all()
            return result
        except Exception as ex:
            raise ex

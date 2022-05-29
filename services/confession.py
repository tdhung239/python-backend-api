# from traceback import print_stack
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func, null
from models.confession import Confession
from schemas.confession import HyboxSchema
from models.user import User
from common.auth import verify


class ConfessionService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_confessions(self):

        try:
            result = self.db_session.query(Confession).filter(Confession.deleted_at == null()). \
                order_by(Confession.created_at.desc())
            confession = [{
                'Id': item.id,
                'Content': item.content,
                'User_id': item.user_id
            } for item in result]

            return confession
        except Exception as error:
            raise error

    def get_user_id(self, email):

        user_id = self.db_session.query(User.id).filter(User.email == str(email)).first()

        return user_id

    async def create_confess(self, confession: HyboxSchema, email):

        id_user = self.get_user_id(email)

        try:
            hy_box = Confession(content=confession.content,
                                user_id=id_user[0], created_at=datetime.now())

            self.db_session.add(hy_box)
            self.db_session.flush()

        except Exception as error:
            raise error



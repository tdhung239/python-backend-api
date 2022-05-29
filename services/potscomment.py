import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.postcomment import CreateCommentSchema, UpdateCommentSchema
from models.postcomment import Potscomment
from models.post import Post
from models.user import User
from sqlalchemy import and_


class PostCommentService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    @staticmethod
    def get_comment_result(result):
        rs = [{
            "id": item.id,
            "id_post": item.post_id,
            "parent_id": item.parent_id,
            "user": {
                "id": item.users_potscomments.profiles_users.id,
                "name": item.users_potscomments.profiles_users.first_name + " "
                        + item.users_potscomments.profiles_users.last_name,
            },
            "content": item.content,
            "created_at": int(item.created_at.strftime('%s'))*1000
        } for item in result]

        return rs

    def get_post_by_id(self, id_post):
        post_id = self.db_session.query(Post).filter(
            Post.id == id_post
        ).first()

        if not post_id:
            raise ValueError(f"Post with id {id_post} not existed")
        return post_id

    def get_cmt_by_id(self, id_post: int, id_cmt: int):
        update_cmt = self.db_session.query(Potscomment).filter(and_(
            Potscomment.post_id == id_post, Potscomment.id == id_cmt
        )).first()

        if not update_cmt:
            raise ValueError(f"id Post {id_post} or id comment {id_cmt} not existed")
        return update_cmt

    def get_user_by_id(self, id_cmt: int, current_user):
        user_id = self.db_session.query(User.id).filter(User.email == current_user).first()

        info_comment = self.db_session.query(Potscomment).filter(and_(
            Potscomment.id == id_cmt, Potscomment.user_id == user_id[0]
        )).first()

        if not info_comment:
            raise ValueError(f"User in cmt id {id_cmt} not existed")

    async def get_post_comments(self, id_post: int, page=None, limit=None):
        try:
            result = self.db_session.query(Potscomment).join(User).filter(
                Potscomment.post_id == id_post
            ).order_by(
                Potscomment.created_at.desc()
            )

            self.get_post_by_id(id_post)

            if page == 1 and limit == 0:
                rs = self.get_comment_result(result)

                return {
                    "data": rs,
                    "total": result.count()
                }
            else:
                result_limit = result.offset(
                    (page - 1) * limit
                ).limit(limit)

                rs = self.get_comment_result(result_limit)
                return {
                    "data": rs,
                    "total": result.count()
                }
        except Exception as ex:
            raise ex

    async def create_post_comments(self, id_post: int, data: CreateCommentSchema, current_user):
        try:
            self.get_post_by_id(id_post)

            user_id = self.db_session.query(User.id).filter(User.email == current_user).first()

            d = datetime.datetime.now().strftime('%s')

            cmt = Potscomment(post_id=id_post, user_id=user_id[0],
                              parent_id=data.parent_id, content=data.content, created_at=datetime.datetime.now())

            self.db_session.add(cmt)
            self.db_session.flush()
            self.db_session.refresh(cmt)
            result = self.db_session.query(Potscomment).join(User).filter(
                Potscomment.id == cmt.id
            )
            print(d)
            rs = self.get_comment_result(result)
            return rs
        except Exception as ex:
            raise ex

    async def update_post_comments(self, id_post: int, id_cmt: int, data: UpdateCommentSchema, current_user):
        try:
            self.get_user_by_id(id_cmt, current_user)
            update_cmt = self.get_cmt_by_id(id_post, id_cmt)

            update_cmt.content = data.content
            update_cmt.updated_at = func.now()

            self.db_session.add(update_cmt)
            self.db_session.flush()

            return "Update successfully"
        except Exception as ex:
            raise ex

    @staticmethod
    def check_id_cmt_parent(list_cmt_all: list, temp: int):
        list_id_cmt = []
        list_cmt = len(list_cmt_all)

        for i in range(0, list_cmt):
            id_cmt = temp
            for index in range(0, list_cmt):
                if id_cmt == list_cmt_all[index]["parent_id"]:
                    list_id_cmt.append(list_cmt_all[index]["id"])
                    temp = list_cmt_all[index]["id"]

        return list_id_cmt

    def delete_comment(self, id_cmt: int):
        comment_delete = self.db_session.query(Potscomment).filter(
            Potscomment.id == id_cmt
        ).first()

        self.db_session.delete(comment_delete)
        self.db_session.flush()

    async def delete_post_comments(self, id_cmt: int, current_user):
        try:
            comment_post_by_id = self.db_session.query(Potscomment).filter(
                Potscomment.id == id_cmt
            ).first()

            if not comment_post_by_id:
                raise ValueError(f"Comment with {id_cmt} not exist")

            self.get_user_by_id(id_cmt, current_user)

            id_cmt_parent_all = self.db_session.query(Potscomment.id, Potscomment.parent_id)
            list_id_cmt_parent_all = list(map(lambda item: dict(item), id_cmt_parent_all))

            list_id_cmt = self.check_id_cmt_parent(list_id_cmt_parent_all, id_cmt)

            for id_duplicate in list_id_cmt:
                self.delete_comment(id_duplicate)
            self.delete_comment(id_cmt)

            return "Delete successfully"
        except Exception as ex:
            raise ex

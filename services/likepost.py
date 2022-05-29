from sqlalchemy.orm import Session
from models.likepost import Likepost
from models.post import Post
from models.user import User
from models.profile import Profile
from sqlalchemy import and_

class LikePostService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_like_posts(self, id_post: int):
        try:
            get_post_id = self.db_session.query(Post).filter(Post.id == id_post).first()
            if not get_post_id:
                raise ValueError(f"Post with id = {id_post} is not existed")

            result = self.db_session.query(Likepost).filter(
                Likepost.post_id == id_post).all()
            rs = [{
                "data": {
                    "id": item.id,
                    "id_user": item.posts_likeusers.id,
                    "first_name": item.posts_likeusers.profiles_users.first_name,
                    "last_name": item.posts_likeusers.profiles_users.last_name,
                }
            } for item in result]
            query = "SELECT count(post_id) as count_like from tbl_likepost where post_id = " + str(id_post) + " "
            total = self.db_session.execute(query).fetchall()[0]["count_like"]
            return {
                "data": rs,
                "total": total
            }
        except Exception as ex:
            raise ex

    async def create_like(self, current_user, id_post: int):
        try:
            check = True
            get_post_id = self.db_session.query(Post).filter(Post.id == id_post).first()
            if not get_post_id:
                raise ValueError(f"Post with id = {id_post} is not existed")

            list_user = self.db_session.query(User.id, Profile.first_name, Profile.last_name).filter(and_(User.email == current_user),(User.id == Profile.user_id)).all()
            dict_user = list(map(lambda x: dict(x), list_user))
            print(dict_user)
            list_like = self.db_session.query(Likepost.id, Likepost.user_id).filter(
                Likepost.post_id == id_post).all()
            dict_like = list(map(lambda x: dict(x), list_like))

            if not dict_like:
                check = False

            for item in dict_like:
                if dict_user[0]["id"] == item["user_id"]:
                    check = True
                    break

                if dict_user[0]["id"] != item["user_id"]:
                    check = False

            if check:
                delete_pf = self.db_session.query(Likepost) \
                    .filter(Likepost.user_id == dict_user[0]["id"]). \
                    filter(Likepost.post_id == id_post).first()
                self.db_session.delete(delete_pf)
                self.db_session.flush()
            else:
                user_update = Likepost(post_id=id_post, like_count=1, user_id=dict_user[0]["id"],
                                       like_user=str(dict_user[0]["first_name"])+str(dict_user[0]["last_name"]))
                self.db_session.add(user_update)
                self.db_session.flush()

        except Exception as ex:
            raise ex

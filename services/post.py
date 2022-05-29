from sqlalchemy import func, null
from sqlalchemy.orm import Session
from models.post import Post
from schemas.post import PostSchema, PostSchemaUpdate
from models.likepost import Likepost
from .category import CategoryService


class PostService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def get_posts(self, catogery_id: int):
        try:
            list_catogery_temp = await CategoryService.get_categorys_parentid(self, catogery_id)
            if list_catogery_temp:
                result = []
                for catogery in list_catogery_temp:
                    rs_temp = await self.find_category(catogery["id"])
                    for posts in rs_temp:
                        result.append(posts)
                result.sort(key=lambda e: e.created_at, reverse=True)
            else:
                result = self.db_session.query(Post) \
                    .filter(Post.deleted_at == null(), Post.category_id == catogery_id) \
                    .order_by(Post.created_at.desc())
            rs = [{
                "id": item.id,
                "title": item.post_title,
                "description": item.post_detail,
                "post_image": item.post_image,
                "category": {
                    "id": item.categorys_posts.id,
                    "name": item.categorys_posts.category_name,
                },
                "like_count": len(item.likeposts_posts),
                "view": item.post_view,
                "created_at": item.created_at
            } for item in result]
            return {
                "data": rs,
                "total": len(rs)
            }
        except Exception as ex:
            raise ex

    async def find_category(self, catogery_id: int):
        try:
            result = self.db_session.query(Post) \
                .filter(Post.deleted_at == null(), Post.category_id == catogery_id)
            return result
        except Exception as ex:
            raise ex

    async def get_post_limit(self, id_category: int, sort_by=None, page=None, limit=None):
        try:
            list_catogery_temp = await CategoryService.get_categorys_parentid(self, id_category)
            if list_catogery_temp:
                result = []
                for catogery in list_catogery_temp:
                    rs_temp = await self.find_category(catogery["id"])
                    for posts in rs_temp:
                        result.append(posts)
                total = len(result)
                if sort_by == "date":
                    result.sort(key=lambda e: e.created_at, reverse=True)
                elif sort_by == "view":
                    result.sort(key=lambda e: e.post_view, reverse=True)
                if page == 1:
                    start = 0
                    end = limit
                else:
                    start = limit * (page - 1)
                    end = limit * page
                result = result[start:end]
            else:
                result = self.db_session.query(Post).filter(Post.deleted_at == null(), Post.category_id == id_category)
                total = result.count()
                if sort_by == "date":
                    result = result.order_by(Post.created_at.desc()).offset((page - 1) * limit).limit(limit)
                elif sort_by == "view":
                    result = result.order_by(Post.post_view.desc()).offset((page - 1) * limit).limit(limit)
                else:
                    result = result.offset((page - 1) * limit).limit(limit)
            rs = [{
                "id": item.id,
                "title": item.post_title,
                "description": item.post_detail,
                "post_image": item.post_image,
                "category": {
                    "id": item.categorys_posts.id,
                    "name": item.categorys_posts.category_name,
                },
                "like_count": len(item.likeposts_posts),
                "view": item.post_view,
                "create_at": item.created_at
            } for item in result]
            return {
                "data": rs,
                "total": total
            }
        except Exception as ex:
            raise ex

    async def create_post(self, data: PostSchema):
        try:
            post = Post(category_id=data.category_id, author_id=data.author_id, post_title=data.post_title,
                        post_image=data.post_image, post_detail_short=data.post_detail_short,
                        post_detail=data.post_detail, post_view=data.post_view, post_hot=data.post_hot,
                        created_at=data.created_at, updated_at=data.updated_at, deleted_at=data.deleted_at)
            self.db_session.add(post)
            self.db_session.flush()
        except Exception as ex:
            raise ex

    async def update_post(self, post_id: int, data: PostSchemaUpdate):
        try:
            post_update = self.db_session.query(Post).filter(Post.id == post_id)
            if not post_update:
                raise ValueError(f"post with {post_id} not exist")
            else:
                post_temp = {}
                for key, value in dict(data).items():
                    if value is not None:
                        post_temp.update({key: value})
                post_update.update(post_temp)
                self.db_session.flush()
        except Exception as ex:
            raise ex

    async def delete_post(self, post_id: int):
        try:
            post_update = self.db_session.query(Post).filter(Post.id == post_id)
            if not post_update:
                raise ValueError(f"post with {post_id} not exist")
            else:
                post_update.update({"deleted_at": func.now()})
        except Exception as ex:
            raise ex

    def get_count_like_post(self, post_id: int):
        get_post_id = self.db_session.query(Post).filter(Post.id == post_id).first()

        if not get_post_id:
            raise ValueError(f"Post with id = {post_id} is not existed")
        total = self.db_session.query(Likepost.like_count).filter(Likepost.post_id == post_id)

        return total.count()

    def get_db_post(self, post_id: int):
        result = self.db_session.query(Post).filter(Post.deleted_at == null()) \
            .filter(Post.id == post_id).first()

        if not result:
            raise ValueError(f"Post Detail with Id={post_id} not exist")
        return result

    def get_update_post_view(self, post_id: int):
        result = self.get_db_post(post_id)
        result.post_view = result.post_view + 1
        self.db_session.add(result)
        self.db_session.flush()

    async def get_post_by_id(self, post_id: int):
        try:

            result = self.get_db_post(post_id)
            self.get_update_post_view(post_id)
            total_like_post = self.get_count_like_post(post_id)

            rs = {
                "id": result.id,
                "title": result.post_title,
                "description": result.post_detail,
                "image": result.post_image,
                "category": {
                    "id": result.categorys_posts.id,
                    "name": result.categorys_posts.category_name,
                },
                "avatar": {
                    "image": result.users_posts.profiles_users.avatar,
                    "name": result.users_posts.profiles_users.first_name + " " +
                            result.users_posts.profiles_users.last_name
                },
                "like_count": total_like_post,
                "view": result.post_view,
                "created_at": int(result.created_at.strftime('%s')) * 1000,
            }
            return rs

        except Exception as error:
            raise error




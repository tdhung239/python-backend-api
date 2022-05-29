from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Post(BaseModel):
    __tablename__ = "tbl_post"
    post_title = Column(String(100))
    post_image = Column(String(255))
    post_detail_short = Column(Text)
    post_detail = Column(Text)
    post_view = Column(Integer)
    post_hot = Column(Integer)
    deleted_at = Column(TIMESTAMP, nullable=True)
    category_id = Column(Integer, ForeignKey("tbl_category.id"), nullable=True)
    author_id = Column(Integer, ForeignKey("tbl_user.id"), nullable=True)
    categorys_posts = relationship("Category", back_populates="posts_categorys", lazy="joined")
    users_posts = relationship("User", back_populates="posts_users", lazy="joined")
    likeposts_posts = relationship("Likepost", back_populates="posts_likeposts", lazy="joined")
    # n-n
    logposts_posts = relationship("Logpost", back_populates="posts_logposts", lazy="joined")
    potscomments_posts = relationship("Potscomment", back_populates="posts_potscomments", lazy="joined")

from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from .base import Base


class Likepost(Base):
    __tablename__ = "tbl_likepost"
    id = Column(Integer, primary_key=True, index=True)
    like_count = Column(Integer)
    like_user = Column(Text)
    post_id = Column(Integer, ForeignKey("tbl_post.id"))
    user_id = Column(Integer, ForeignKey("tbl_user.id"))
    posts_likeposts = relationship("Post", back_populates="likeposts_posts", lazy="joined")
    posts_likeusers = relationship("User", back_populates="likeusers_posts", lazy="joined")

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, SmallInteger, TIMESTAMP, func, Text, Table
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from .base import BaseModel


class Potscomment(BaseModel):
    __tablename__ = "tbl_postcomment"
    parent_id = Column(Integer)
    content = Column(Text)
    post_id = Column(Integer, ForeignKey("tbl_post.id"))
    user_id = Column(Integer, ForeignKey("tbl_user.id"))
    posts_potscomments = relationship("Post", back_populates="potscomments_posts")
    users_potscomments = relationship("User", back_populates="potscomments_users")

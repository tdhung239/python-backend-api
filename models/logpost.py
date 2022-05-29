from sqlalchemy import Column, String, Integer, ForeignKey, Enum, SmallInteger, TIMESTAMP, func, Text, Table
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from .base import BaseModel


class Logpost(BaseModel):
    __tablename__ = "tbl_logpost"
    action = Column(String(50))
    note = Column(Text)
    post_id = Column(Integer, ForeignKey("tbl_post.id"))
    user_id = Column(Integer, ForeignKey("tbl_user.id"))
    posts_logposts = relationship("Post", back_populates="logposts_posts")
    users_logposts = relationship("User", back_populates="logposts_users")

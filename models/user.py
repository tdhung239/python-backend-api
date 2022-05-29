from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "tbl_user"
    user_name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    token = Column(String(255), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    role_id = Column(Integer, ForeignKey("tbl_role.id"), nullable=True)
    roles = relationship("Role", back_populates="users", lazy="joined")
    profiles_users = relationship("Profile", back_populates="users_profiles", lazy="joined", uselist=False)
    posts_users = relationship("Post", back_populates="users_posts", lazy="joined")
    confessions_users = relationship("Confession", back_populates="users_confessions", lazy="joined")
    # n-n
    logposts_users = relationship("Logpost", back_populates="users_logposts", lazy="joined")
    potscomments_users = relationship("Potscomment", back_populates="users_potscomments", lazy="joined")
    likeusers_posts = relationship("Likepost", back_populates="posts_likeusers", lazy="joined")

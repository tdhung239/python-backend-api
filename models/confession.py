from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text, TIMESTAMP, func
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship

from .base import BaseModel


class Confession(BaseModel):
    __tablename__ = "tbl_confession"
    content = Column(Text)
    deleted_at = Column(TIMESTAMP, nullable=True)
    user_id = Column(Integer, ForeignKey("tbl_user.id"))
    users_confessions = relationship("User", back_populates="confessions_users", lazy="joined")

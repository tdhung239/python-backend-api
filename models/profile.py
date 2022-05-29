import enum

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, SmallInteger, TIMESTAMP, func, Date
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship

from .base import BaseModel


class Profile(BaseModel):
    __tablename__ = "tbl_profile"
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    gender = Column(Enum('other', 'male', 'female'), nullable=False)
    phone = Column(String(20), nullable=False)
    avatar = Column(String(255))
    date_of_birth = Column(Date)
    count_post = Column(SmallInteger)
    address = Column(String(255))
    deleted_at = Column(TIMESTAMP, nullable=True)
    user_id = Column(Integer, ForeignKey("tbl_user.id"))
    users_profiles = relationship("User", back_populates="profiles_users", lazy="joined")

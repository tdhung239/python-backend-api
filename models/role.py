from sqlalchemy import Column, String, Integer, ForeignKey, Enum, Text
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship

from .base import BaseModel, Base


class Role(Base):
    __tablename__ = "tbl_role"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), nullable=False)
    role_description = Column(Text, nullable=False)
    users = relationship("User", back_populates="roles", lazy="joined")

import enum

from sqlalchemy import Column, String, Integer, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import relationship

from .base import BaseModel


class Banner(BaseModel):
    __tablename__ = "tbl_banner"
    banner_type = Column(Enum('image', 'video'))
    banner_path = Column(String(255))
    title = Column(String(255))
    disable = Column(Integer)

    bannershows_banners = relationship("Bannershow", back_populates="banners_bannershows", lazy="joined")

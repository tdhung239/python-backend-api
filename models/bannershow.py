from sqlalchemy import Column, String, Integer, ForeignKey, Enum, SmallInteger, TIMESTAMP, func, Text, Table
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import relationship
from .base import BaseModel, Base


class Bannershow(Base):
    __tablename__ = "tbl_banner_show"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("tbl_category.id"), nullable=True)
    banner_id = Column(Integer, ForeignKey("tbl_banner.id"), nullable=True)
    categorys_bannershows = relationship("Category", back_populates="bannershows_categorys", lazy="joined")
    banners_bannershows = relationship("Banner", back_populates="bannershows_banners", lazy="joined")

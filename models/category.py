from sqlalchemy import Column, String, Integer, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import BaseModel


class Category(BaseModel):
    __tablename__ = "tbl_category"
    category_name = Column(String(30), nullable=False)
    parent_id = Column(Integer, nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    posts_categorys = relationship("Post", back_populates="categorys_posts", lazy="joined")
    bannershows_categorys = relationship("Bannershow", back_populates="categorys_bannershows", lazy="joined")

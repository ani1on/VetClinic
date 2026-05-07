from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship

from .base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    description = Column(String)
    price = Column(Float)
    category = Column(String(100))
    stock_quantity = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    image_url = Column(String(300))
    favorites = relationship(
        "Favorite",
        primaryjoin="and_(Product.id == Favorite.entity_id, Favorite.entity_type == 'product')",
        foreign_keys="[Favorite.entity_id]",
        viewonly=True
    )
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")
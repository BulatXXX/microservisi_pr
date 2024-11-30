from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    products = relationship("Product", back_populates="category")



class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    expiry_date = Column(Date, nullable=True)

    category = relationship("Category", back_populates="products")



class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("supply_lists.id"))
    creation_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

    supply_list = relationship("SupplyList", back_populates="deliveries")



class SupplyList(Base):
    __tablename__ = "supply_lists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    item_count = Column(Integer, nullable=False)

    deliveries = relationship("Delivery", back_populates="supply_list")

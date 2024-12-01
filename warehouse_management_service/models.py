from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(String(255), nullable=False)


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    name = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    expiry_date = Column(Date, nullable=True)

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    title = Column(String(255), nullable=False)
    list = Column(Text)
    creation_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)





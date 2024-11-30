from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# Схемы для Category
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# Схемы для Product
class ProductBase(BaseModel):
    name: str
    category_id: int
    expiry_date: Optional[datetime]

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        orm_mode = True


# Схемы для SupplyList
class SupplyListBase(BaseModel):
    name: str
    item_count: int

class SupplyListCreate(SupplyListBase):
    pass

class SupplyListResponse(SupplyListBase):
    id: int

    class Config:
        orm_mode = True


# Схемы для Delivery
class DeliveryBase(BaseModel):
    list_id: int
    creation_date: datetime
    status: str
    description: Optional[str]

class DeliveryCreate(DeliveryBase):
    pass

class DeliveryResponse(DeliveryBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

# Схемы для Product
class ProductBase(BaseModel):
    name: str
    category_id: int
    expiry_date: Optional[datetime] = None

class ProductCreate(ProductBase):
    pass

class DeliveryCreate(BaseModel):
    title: str
    list: str  # Сохраняем список в формате JSON строки
    status: str = "Pending"  # Можно указать статус по умолчанию
    description: str = None
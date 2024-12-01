from datetime import datetime, timedelta
from typing import List

import requests
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

from sqlalchemy import func

from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session, aliased
from models import Product, Delivery, Category
from schema import CategoryCreate, ProductCreate, CategoryUpdate,DeliveryCreate

app = FastAPI(title="/warehouse Management Service")
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/test")
async def test():
    return "OK-2"


@app.post("/warehouse/categories")
async def create_category(category: CategoryCreate, db: db_dependency):
    if category.name == "":
        raise HTTPException(
            status_code=400,
            detail="The category name cannot be empty",
        )
    new_category = Category(name=category.name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"id": new_category.id}


@app.get("/warehouse/categories")
async def get_categories(db: db_dependency, offset: int = 0, count: int = 0):
    if offset < 0 or count < 0:
        raise HTTPException(status_code=400, detail="Bad paging parameters")
    if count == 0:
        categories = db.query(Category).offset(offset).all()
    else:
        categories = db.query(Category).offset(offset).limit(count).all()

    categories_with_product_count = []
    for category in categories:
        product_count = db.query(Product).filter(Product.category_id == category.id).count()
        category_data = category.__dict__
        category_data['product_count'] = product_count
        categories_with_product_count.append(category_data)

    return categories_with_product_count


@app.get("/warehouse/categories/{category_id}")
async def get_category(category_id: int, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    product_count = db.query(Product).filter(Product.category_id == category.id).count()
    category.__dict__['product_count'] = product_count
    return category


@app.delete("/warehouse/categories/{category_id}")
async def get_category(category_id: int, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()

@app.patch("/warehouse/categories/{category_id}")
async def get_category(category_id: int,category_data: CategoryUpdate, db: db_dependency,):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    category.name = category_data.name
    db.commit()
    db.refresh(category)
    return category


@app.post("/warehouse/items")
async def create_item(item_data: ProductCreate, db: db_dependency):
    category = db.query(Category).filter(Category.id == item_data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    item = Product(name=item_data.name, category_id=item_data.category_id,expiry_date=item_data.expiry_date)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id}

@app.get("/warehouse/items")
async def get_products(db: db_dependency, offset: int = 0, count: int = 0):
    if offset < 0 or count < 0:
        raise HTTPException(status_code=400, detail="Bad paging parameters")
    if count == 0:
        items = db.query(Product).offset(offset).all()
    else:
        items = db.query(Product).offset(offset).limit(count).all()
    return items


@app.get("/warehouse/items/{item_id}")
def get_product(item_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.id == item_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/supply/list")
async def create_delivery(delivery: DeliveryCreate, db: Session = Depends(get_db)):
    new_delivery = Delivery(
        title=delivery.title,
        list=delivery.list,
        creation_date=datetime.utcnow(),
        status=delivery.status,
        description=delivery.description
    )
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)


    task_data = {
        "title": f"Принять доставку: {new_delivery.title}",
        "description": f"Delivery created with ID {new_delivery.id}",
        "datetime": (datetime.now() + timedelta(days=2)).isoformat(),  # Преобразуем в формат ISO 8601
    }

    # Отправка задачи на другой сервис
    task_response = requests.post("http://127.0.0.1:8000/tasks", json=task_data)  # Другой сервис работает на порту 8000

    if task_response.status_code != 200:
        raise HTTPException(status_code=task_response.status_code, detail=task_response.text)

    return {"delivery_id": new_delivery.id, "task_status": "Created successfully"}


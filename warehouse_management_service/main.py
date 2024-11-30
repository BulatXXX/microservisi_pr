from datetime import datetime, timedelta
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from models import Product, SupplyList, Delivery, Category
from schema import CategoryResponse, CategoryCreate, ProductResponse, ProductCreate, SupplyListResponse, \
    SupplyListCreate, DeliveryResponse, DeliveryCreate

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
@app.get("/warehouse/categories", response_model=List[CategoryResponse])
def get_categories(db: db_dependency):
    return db.query(Category).all()


@app.post("/warehouse/categories", response_model=CategoryResponse)
def create_category(category: CategoryCreate, db: db_dependency):
    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@app.get("/warehouse/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/warehouse/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: db_dependency):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/warehouse/items", response_model=List[ProductResponse])
def get_products(db: db_dependency):
    return db.query(Product).all()


@app.post("/warehouse/items", response_model=ProductResponse)
def create_product(product: ProductCreate, db: db_dependency):
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@app.get("/warehouse/items/{item_id}", response_model=ProductResponse)
def get_product(product_id: int, db: db_dependency):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product






#####EVERYTHING AFTER THIS MUST BE CHECKED
#TODO:WRONG REQUEST
@app.get("/supply/list", response_model=List[SupplyListResponse])
def get_supply_lists(db: db_dependency):
    return db.query(SupplyList).all()

#TODO:NOT CHECKED REQUEST
@app.post("/supply/list", response_model=SupplyListResponse)
def create_supply_list(supply_list: SupplyListCreate, db: db_dependency):
    new_list = SupplyList(**supply_list.dict())
    db.add(new_list)
    db.commit()
    db.refresh(new_list)
    return new_list


@app.get("/supply_lists/{supply_list_id}", response_model=SupplyListResponse)
def get_supply_list(supply_list_id: int, db: db_dependency):
    supply_list = db.query(SupplyList).filter(SupplyList.id == supply_list_id).first()
    if not supply_list:
        raise HTTPException(status_code=404, detail="Supply List not found")
    return supply_list


@app.get("/deliveries/", response_model=List[DeliveryResponse])
def get_deliveries(db: db_dependency):
    return db.query(Delivery).all()


@app.post("/deliveries/", response_model=DeliveryResponse)
def create_delivery(delivery: DeliveryCreate, db: db_dependency):
    new_delivery = Delivery(**delivery.dict())
    db.add(new_delivery)
    db.commit()
    db.refresh(new_delivery)
    return new_delivery


@app.get("/deliveries/{delivery_id}", response_model=DeliveryResponse)
def get_delivery(delivery_id: int, db: db_dependency):
    delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    return delivery

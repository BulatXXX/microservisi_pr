from fastapi import FastAPI

from app.database import engine, Base
from app.routers import tasks_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Staff Management API")

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
app.include_router(tasks_router.router)



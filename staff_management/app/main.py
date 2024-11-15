from fastapi import FastAPI

from staff_management.app.database import engine, Base
from staff_management.app.routers import tasks_router


app = FastAPI(title="Staff Management API")

@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
app.include_router(tasks_router.router)



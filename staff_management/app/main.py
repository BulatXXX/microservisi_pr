from threading import Thread

from fastapi import FastAPI

from app.database import engine, Base
from app.routers import tasks_router

from app.rabbitmq import consume_messages

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Staff Management API")


def start_rabbitmq_listener():
    Thread(target=consume_messages, daemon=True).start()

start_rabbitmq_listener()
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
app.include_router(tasks_router.router)



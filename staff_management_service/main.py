from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated
from database import engine, SessionLocal, Base
from sqlalchemy.orm import Session
from models import Task, TaskStatus, Staff
from schema import TaskCreate, TaskResponse, TaskAssign

app = FastAPI(title="Staff Management Service")
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
    return {"OK"}


@app.get("/tasks")
async def get_tasks(db: db_dependency, offset: int = 0, count: int = 0):
    if offset < 0 or count < 0:
        raise HTTPException(status_code=400, detail="Bad paging parameters")
    if count == 0:
        result = db.query(Task).offset(offset).all()
    else:
        result = db.query(Task).offset(offset).limit(count).all()
    return result


@app.post("/tasks")
async def create_task(task: TaskCreate, db: db_dependency):
    if task.datetime <= datetime.now() + timedelta(hours=1):
        raise HTTPException(
            status_code=400,
            detail="Task datetime must be at least 1 hour in the future."
        )
    db_task = Task(
        title=task.title,
        description=task.description,
        datetime=task.datetime,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return {"id": db_task.id, "status": db_task.status}


@app.patch("/tasks/{id}/assign")
async def assign_task(id: int, assign_data: TaskAssign, db: db_dependency):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == TaskStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Cannot assign a completed task")

    staff = db.query(Staff).filter(Staff.id == assign_data.assigned_to).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    overlapping_task = (
        db.query(Task)
        .filter(Task.assigned_to == assign_data.assigned_to)
        .filter(Task.status == TaskStatus.ASSIGNED)
        .filter(
            (Task.datetime >= task.datetime - timedelta(hours=1))
            & (Task.datetime <= task.datetime + timedelta(hours=1))
        )
        .first()
    )
    if overlapping_task:
        raise HTTPException(
            status_code=409,
            detail="Staff member is not available for this task due to overlapping assignments."
        )
    task.assigned_to = assign_data.assigned_to
    task.status = TaskStatus.ASSIGNED
    db.commit()
    db.refresh(task)
    return {"id": task.id, "status": task.status}


@app.patch("/tasks/{id}/complete", tags=["Staff Management"])
def complete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == TaskStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Task is already completed")

    task.status = TaskStatus.COMPLETED
    db.commit()
    db.refresh(task)
    return {"id": task.id, "status": task.status}


@app.get("/tasks/{id}", tags=["Staff Management"])
def get_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        datetime=task.datetime,
        assigned_to=task.assigned_to,
        status=task.status,
    )

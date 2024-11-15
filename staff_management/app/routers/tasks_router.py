from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from staff_management.app.database import get_db
from staff_management.app.models.task import Task, TaskStatus, Staff
from pydantic import BaseModel
from datetime import datetime, timedelta

from staff_management.app.schemas.task_schema import TaskResponse, TaskCreate

router = APIRouter()

# Схема для назначения задачи сотруднику
class AssignTask(BaseModel):
    assigned_to: int


# 1. Получение списка задач
@router.get("/tasks", tags=["Staff Management"])
def get_tasks(offset: int = 0, count: int = 10, db: Session = Depends(get_db)):
    tasks = db.query(Task).offset(offset).limit(count).all()
    return tasks


# 2. Создание новой задачи
@router.post("/tasks", tags=["Staff Management"])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    new_task = Task(
        title=task.title,
        description=task.description,
        datetime=task.datetime,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"id": new_task.id, "status": "Created"}


# 3. Назначение задачи сотруднику
@router.patch("/tasks/{id}/assign", tags=["Staff Management"])
def assign_task(id: int, assign_data: AssignTask, db: Session = Depends(get_db)):
    # Проверка существования задачи
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == TaskStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Cannot assign a completed task")

    # Проверка существования сотрудника
    staff = db.query(Staff).filter(Staff.id == assign_data.assigned_to).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")

    # Проверка пересечений задач
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

    # Назначение задачи
    task.assigned_to = assign_data.assigned_to
    task.status = TaskStatus.ASSIGNED
    db.commit()
    db.refresh(task)
    return {"id": task.id, "status": task.status.value}


# 4. Завершение задачи
@router.patch("/tasks/{id}/complete", tags=["Staff Management"])
def complete_task(id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status == TaskStatus.COMPLETED:
        raise HTTPException(status_code=409, detail="Task is already completed")

    task.status = TaskStatus.COMPLETED
    db.commit()
    db.refresh(task)
    return {"id": task.id, "status": task.status.value}


# 5. Получение информации о задаче
@router.get("/tasks/{id}", tags=["Staff Management"])
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
        status=task.status.value,
    )


@router.get("/test")
def test():
    return [
        TaskResponse(
            id=1,
            title="Уборка в номере",
            description="Необходимо убрать номер",
            datetime="2024-11-02 10:00:00",
            assigned_to=32896,
            status="Назначена"
        ),
        TaskResponse(
            id=2,
            title="Проверка оборудования",
            description="Необходимо проверить работоспособность кондиционеров",
            datetime="2024-11-03 14:00:00",
            assigned_to=None,
            status="Создана"
        )
    ]

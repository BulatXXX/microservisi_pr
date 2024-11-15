from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, validator
from datetime import datetime, timedelta


from app.models.task import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str
    datetime: datetime
    status: TaskStatus = TaskStatus.CREATED

    @validator("datetime")
    def validate_datetime(cls, value):
        if value <= datetime.now() + timedelta(hours=1):
            raise HTTPException(
                status_code=400,
                detail="Task datetime must be at least 1 hour in the future."
            )
        return value

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    datetime: datetime
    assigned_to: Optional[int]
    status: str

class TaskAssign(BaseModel):
    assigned_to: int
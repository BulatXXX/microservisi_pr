from typing import Optional

from pydantic import BaseModel
from datetime import datetime
from models import TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: str
    datetime: datetime
    status: str = TaskStatus.CREATED

class TaskAssign(BaseModel):
    assigned_to: int

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    datetime: datetime
    assigned_to: Optional[int]
    status: str

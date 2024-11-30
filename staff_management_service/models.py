from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey, Enum
from database import Base

class TaskStatus(Enum):
    CREATED = "Created"
    ASSIGNED = "Assigned"
    COMPLETED = "Completed"

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    datetime = Column(TIMESTAMP)
    assigned_to = Column(Integer, nullable=True)
    status = Column(String(255), default=TaskStatus.CREATED, nullable=False)

class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=False)

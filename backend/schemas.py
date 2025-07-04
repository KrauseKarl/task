from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field, field_validator

from models import StatenEnum


class ServiceBase(BaseModel):
    title: str = Field(..., max_length=120, min_length=3)
    description: str | None = Field(None, max_length=450)
    priority: StatenEnum
    due_date: datetime = Field(
        ...,
        description="Format: YYYY-MM-DD HH:MM",
        examples=["2025-05-20 11:30"]
    )
    done: bool = False

    @field_validator('due_date', mode='before')
    def parse_due_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M")
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM")
        return value

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M") if v else None
        })


class TaskRequest(ServiceBase):
    pass


class TaskUpdateRequest(ServiceBase):
    pass


class TaskItemResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime | None


class TasksResponse(BaseModel):
    tasks: List[TaskItemResponse]


class StatusResponse(BaseModel):
    status: str
    updated: bool
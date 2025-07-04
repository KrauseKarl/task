from typing import Sequence, Any, Coroutine, Optional
from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import ScalarResult
from sqlalchemy.exc import SQLAlchemyError

from db.database import Database
from db.handler import DataBaseHandler
from models import ServiceModel, HistoryModel
from schemas import *


class TasksService:
    def __init__(self, db: Database):
        self.db = db

    async def list_tasks(self) -> Sequence[ServiceModel]:
        try:
            async with self.db.get_session() as session:
                    repo = DataBaseHandler(session)
                    return await repo.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Failed to list tasks: {str(e)}"
            )

    async def get_task(self, task_id: int) -> Optional[ServiceModel]:
        try:
            async with self.db.get_session() as session:
                repo = DataBaseHandler(session)
                task =  await repo.get(task_id)
                if not task:
                    raise HTTPException(status_code=404, detail="Task not found")
                return task
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Failed to get task: {str(e)}"
            )

    async def create_task(self, request: TaskRequest) -> ServiceModel:
        try:
            task_data = ServiceModel(
                title=request.title,
                description=request.description,
                priority=request.priority,
                due_date=request.due_date,
                done=request.done
            )
            async with self.db.get_session() as session:
                repo = DataBaseHandler(session)
                await repo.create(task_data)
                await session.refresh(task_data)
                return task_data
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create task: {str(e)}"
            )

    async def change_status(self, task_id: int, status_done: bool) -> StatusResponse:
        try:
            async with self.db.get_session() as session:
                repo = DataBaseHandler(session)
                updated = await repo.change_done_status(task_id, status_done)

                if not updated:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found"
                    )

                return StatusResponse(status='success', updated=True)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update task status: {str(e)}"
            )

    async def update_task(self, task_id: int, data: TaskUpdateRequest) -> StatusResponse:
        try:
            async with self.db.get_session() as session:
                repo = DataBaseHandler(session)
                updated = await repo.update(task_id, data)

                if not updated:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found"
                    )
                return StatusResponse(status='success', updated=True)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to update task: {str(e)}"
            )


    async def delete_task(self, task_id: int) -> StatusResponse:
        try:
            async with self.db.get_session() as session:
                repo = DataBaseHandler(session)
                deleted = await repo.delete(task_id)
                if not deleted:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Task not found"
                    )
                return StatusResponse(status='success', updated=True)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete task: {str(e)}"
            )
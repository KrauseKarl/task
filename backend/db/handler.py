from typing import Optional, Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import ServiceModel


class DataBaseHandler:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: ServiceModel) -> None:
        try:
            self.session.add(task)
            await self.session.flush()
            await self.session.refresh(task)
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to create task: {str(e)}")

    async def get(self, task_id: int) -> Optional[ServiceModel]:
        try:
            task_data = await self.session.execute(
                select(ServiceModel)
                .where(ServiceModel.id == task_id)
            )
            task_data = task_data.scalars().first()
            return task_data
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to get task: {str(e)}")

    async def change_done_status(self, task_id: int, is_done: bool) -> int:
        try:
            res = await self.session.execute(
                update(ServiceModel)
                .where(ServiceModel.id == task_id)
                .values(done=is_done)
            )
            await self.session.commit()
            return res.rowcount
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ValueError(f"Failed to update task status: {str(e)}")

    async def get_all(self) -> Sequence[ServiceModel]:
        try:
            res = await self.session.execute(
                select(ServiceModel)
                .order_by(
                    ServiceModel.done,
                    ServiceModel.priority.desc(),
                    ServiceModel.due_date,
                )
            )
            return res.scalars().all()
        except SQLAlchemyError as e:
            raise ValueError(f"Failed to fetch tasks: {str(e)}")

    async def update(self, task_id: int, data: ServiceModel) -> int:
        try:
            res = await self.session.execute(
                update(ServiceModel)
                .where(ServiceModel.id == task_id)
                .values(
                    title=data.title,
                    description=data.description,
                    priority=data.priority.value,
                    due_date=data.due_date,
                    done=data.done,
                )
            )
            await self.session.commit()
            return res.rowcount
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ValueError(f"Failed to update task: {str(e)}")

    async def delete(self, task_id: int) -> int:
        try:
            res = await self.session.execute(
                delete(ServiceModel)
                .where(ServiceModel.id == task_id)
            )
            await self.session.commit()
            return res.rowcount
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ValueError(f"Failed to delete task: {str(e)}")
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import *
from crud import TasksService
# from core import get_tasks_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get('/',)
async def get_all_services(service: TasksService = Depends(get_tasks_service)):
    try:
        tasks = await service.list_tasks()
        return TasksResponse(
            tasks=[TaskItemResponse.model_validate(task.__dict__) for task in tasks]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#
# @router.get("/{task_id}", response_model=TaskItemResponse)
# async def get_task(
#         task_id: int,
#         service: TasksService = Depends(get_tasks_service),
# ) -> TaskItemResponse:
#     try:
#         task = await service.get_task(task_id)
#         if not task:
#             raise HTTPException(status_code=404, detail="Task not found")
#         return TaskItemResponse.model_validate(task.__dict__)
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @router.post('/', response_model=TaskItemResponse)
# async def create_task(
#         request: TaskRequest,
#         service: TasksService = Depends(get_tasks_service)
# ) -> TaskItemResponse:
#     try:
#         task = await service.create_task(request)
#         return TaskItemResponse.model_validate(task.__dict__)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @router.post("/{task_id}/complete", response_model=StatusResponse)
# async def set_task_complete(
#         task_id: int,
#         status: bool = Query(..., description="New completion status"),
#         service: TasksService = Depends(get_tasks_service),
# ) -> StatusResponse:
#     try:
#         return await service.change_status(task_id, status)
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @router.put("/{task_id}", response_model=StatusResponse)
# async def update_task(
#         task_id: int,
#         updated_data: TaskUpdateRequest,
#         service: TasksService = Depends(get_tasks_service),
# ) -> StatusResponse:
#     try:
#         return await service.update_task(task_id, updated_data)
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
# @router.delete("/{task_id}", response_model=StatusResponse)
# async def delete_task(
#         task_id: int,
#         service: TasksService = Depends(get_tasks_service),
# ) -> StatusResponse:
#     try:
#         return await service.delete_task(task_id)
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
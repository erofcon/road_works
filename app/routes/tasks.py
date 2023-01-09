import os
from datetime import datetime
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Body, File, Form, status

from app.crud import users as users_crud
from app.crud import tasks as tasks_crud
from app.crud import task_images as task_images_crud
from app.schemas import users as users_schemas
from app.schemas import tasks as tasks_schemas
from app.schemas import task_images as task_images_schemas

router = APIRouter()


@router.post('/create_task')
async def create_task(description: str = Form(default=None), lead_datetime: datetime = Form(),
                      latitude: float = Form(default=None), longitude: float = Form(default=None),
                      executor_id: int = Form(), group_id: int = Form(),
                      files: list[UploadFile] | None = File(None),
                      current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    task = tasks_schemas.CreateTask(description=description, lead_datetime=lead_datetime, latitude=latitude,
                                    longitude=longitude, executor_id=executor_id, group_id=group_id)

    task_id = await tasks_crud.create_task(task=task, creator_id=current_user.id)
    if not task_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if files:
        try:
            file_path = f'static/task_images/{datetime.now().strftime("%Y-%m-%d")}'
            if not os.path.isdir(file_path):
                os.makedirs(file_path)

            for file in files:
                file_name = f'{file_path}/{file.filename}'
                if file.content_type in ['image/jpeg', 'image/png']:
                    with open(file_name, 'wb') as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    await task_images_crud.create_task_images(
                        task=task_images_schemas.TaskImagesCreate(url=file_name, task_id=task_id))
        except Exception:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/current_tasks', response_model=list[tasks_schemas.CurrentTasks])
async def get_current_tasks(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await tasks_crud.get_current_tasks(current_user.id)


@router.get('/expired_tasks', response_model=list[tasks_schemas.CurrentTasks])
async def get_expired_tasks(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await tasks_crud.get_expired_tasks(current_user.id)


@router.get('/all_tasks', response_model=list[tasks_schemas.CurrentTasks])
async def get_all_tasks(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await tasks_crud.get_all_tasks(current_user.id)


@router.get('/get_task')
async def get_task(task_id: int, current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await tasks_crud.get_task(task_id=task_id, current_user=current_user)

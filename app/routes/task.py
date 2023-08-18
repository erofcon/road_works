import os
from datetime import datetime
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi_pagination import Page, paginate, Params

from app.crud import task as task_crud
from app.crud import task_images as task_images_crud
from app.schemas import task as task_schemas
from app.schemas import task_images as task_images_schemas
from app.crud import user as user_crud
from app.crud import group as groups_crud
from app.schemas import user as user_schemas

router = APIRouter()


@router.post('/create_task')
async def create_task(description: str = Form(default=None), lead_datetime: datetime = Form(),
                      latitude: float = Form(default=None), longitude: float = Form(default=None),
                      executor_id: int = Form(), group_id: int = Form(),
                      files: list[UploadFile] | None = File(None),
                      current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    """
    :param description:
    :param lead_datetime:
    :param latitude:
    :param longitude:
    :param executor_id:
    :param group_id:
    :param files:
    :param current_user:
    :return:
    """

    if not current_user.is_creator:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    related_groups = await groups_crud.get_related_groups(user_id=current_user.id)
    current_groups = filter(lambda element: element.id == group_id, related_groups)

    if not list(current_groups):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    related_executor_users = await user_crud.get_related_executor_users(group_id=group_id)
    current_executor_users = filter(lambda element: element.id == executor_id, related_executor_users)

    if not list(current_executor_users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    task = task_schemas.CreateTask(description=description, lead_datetime=lead_datetime, latitude=latitude,
                                   longitude=longitude, executor_id=executor_id, group_id=group_id)

    task_id = await task_crud.create_task(task=task, creator_id=current_user.id)
    if not task_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if files:
        try:
            file_path = f'static/task_images/{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}'
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


@router.get('/current_tasks', response_model=Page[task_schemas.CurrentTask])
async def get_current_tasks(params: Params = Depends(),
                            current_user: user_schemas.UserWithCheckCreatorStatus = Depends(
                                user_crud.get_current_user)):
    if current_user.is_admin:
        return paginate(await task_crud.get_current_tasks_for_admin(), params)

    return paginate(await task_crud.get_current_tasks(current_user.id), params)


@router.get('/expired_tasks', response_model=Page[task_schemas.CurrentTask])
async def get_expired_tasks(params: Params = Depends(),
                            current_user: user_schemas.UserWithCheckCreatorStatus = Depends(
                                user_crud.get_current_user)):
    if current_user.is_admin:
        return paginate(await task_crud.get_expired_tasks_for_admin(), params)

    return paginate(await task_crud.get_expired_tasks(current_user.id), params)


@router.get('/all_tasks', response_model=Page[task_schemas.CurrentTask])
async def get_all_tasks(params: Params = Depends(),
                        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin:
        return paginate(await task_crud.get_all_tasks_for_admin(), params)

    return paginate(await task_crud.get_all_tasks(current_user.id), params)


@router.get('/done_tasks', response_model=Page[task_schemas.CurrentTask])
async def get_done_tasks(params: Params = Depends(),
                         current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin:
        return paginate(await task_crud.get_done_tasks_for_admin(), params)

    return paginate(await task_crud.get_done_tasks(current_user.id), params)


@router.get('/get_task')
async def get_task(task_id: int,
                   current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    return await task_crud.get_task(task_id=task_id, current_user=current_user)


@router.get('/close_task')
async def close_task(task_id: int,
                     current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    task = await task_crud.get_base_task(task_id)

    if not task or not current_user.is_admin and not task.creator_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    await task_crud.close_task(task_id=task_id)

    return await task_crud.get_task(task_id=task_id, current_user=current_user)


@router.get('/get_task_with_location')
async def get_task_with_location(latitude: float, longitude: float,
                                 current_user: user_schemas.UserWithCheckCreatorStatus = Depends(
                                     user_crud.get_current_user)):
    if current_user.is_admin:
        return await task_crud.get_task_with_location_for_admin(latitude=latitude, longitude=longitude)
    return await task_crud.get_task_with_location(latitude=latitude, longitude=longitude,
                                                  user_id=current_user.id)


@router.get('/get_last_current_task_with_image')
async def get_last_current_task_with_image(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin:
        return await task_crud.get_last_current_task_with_image_for_admin()

    return await task_crud.get_last_current_task_with_image(user_id=current_user.id)


@router.get('/get_task_statistic')
async def get_task_statistic(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin:
        return await task_crud.get_task_statistic_for_admin()
    return await task_crud.get_task_statistic_for_user(user_id=current_user.id)

from fastapi import APIRouter, Depends

from app.crud import user as user_crud

from app.crud import map as map_crud
from app.crud import detection as detections_crud
from app.schemas import user as user_schemas

router = APIRouter()


@router.get('/get_geo_json_done_tasks')
async def get_geo_json_done_tasks(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin:
        return await map_crud.get_geo_json_done_tasks_for_admin()

    return await map_crud.get_geo_json_done_tasks(current_user.id)


@router.get('/get_geo_json_expired_tasks')
async def get_geo_json_expired_tasks(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin:
        await map_crud.get_geo_json_expired_tasks_for_admin()

    return await map_crud.get_geo_json_expired_tasks(current_user.id)


@router.get('/get_geo_json_current_tasks')
async def get_geo_json_current_tasks(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin:
        return await map_crud.get_geo_json_current_tasks_for_admin()
    return await map_crud.get_geo_json_current_tasks(current_user.id)


@router.get('/get_all_detection_for_map')
async def get_all_detection_for_map(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin or current_user.is_creator:
        return await detections_crud.get_all_detection_with_locations_for_groups_users(creator_id=current_user.id)

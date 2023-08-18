import os
import shutil
from datetime import datetime

from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends, status

from app.schemas import user as user_schemas
from app.crud import user as user_crud
from app.crud import detection as detection_crud
from app.schemas import detection as detection_schemas
import celery_worker

router = APIRouter()


@router.post('/run_detection_with_xml')
async def run_detection_with_xml(video_file: UploadFile, xml_file: UploadFile, description: str = Form(default=None),
                                 current_user: user_schemas.UserWithCheckCreatorStatus = Depends(
                                     user_crud.get_current_user)):
    if not current_user.is_creator:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    files_path = f'static/detection_files/detection_with_xml/{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}/upload_files'

    if not os.path.isdir(files_path):
        os.makedirs(files_path)

    video_path = f'{files_path}/{video_file.filename}'
    xml_path = f'{files_path}/{xml_file.filename}'

    with open(video_path, 'wb') as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    with open(xml_path, 'wb') as buffer:
        shutil.copyfileobj(xml_file.file, buffer)

    celery_worker.run_detection_with_xml.delay(video_path=video_path, xml_path=xml_path, creator_id=current_user.id,
                                               description=description)

    return HTTPException(status_code=status.HTTP_200_OK)


@router.post('/run_detection_with_tracker')
async def run_detection_with_tracker(video_file: UploadFile, video_start_datetime: datetime = Form(),
                                     description: str = Form(default=None),
                                     current_user: user_schemas.UserWithCheckCreatorStatus = Depends(
                                         user_crud.get_current_user)):
    if not current_user.is_creator:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    files_path = f'static/detection_files/detection_with_tracker/{datetime.now().strftime("%Y-%m-%dT%H-%M-%S")}/upload_files'

    if not os.path.isdir(files_path):
        os.makedirs(files_path)

    video_path = f'{files_path}/{video_file.filename}'

    with open(video_path, 'wb') as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    celery_worker.run_detection_with_tracker.delay(creator_id=current_user.id, video_path=video_path,
                                                   video_start_datetime=video_start_datetime, description=description)

    return HTTPException(status_code=status.HTTP_200_OK)


@router.get('/get_all_detections', response_model=list[detection_schemas.DetectionWithUserName])
async def get_all_detections(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    """
    :param current_user:
    :return:
    """

    if current_user.is_admin:
        return await detection_crud.get_all_detections_for_admin()

    elif current_user.is_creator:
        return await detection_crud.get_all_detections_for_creator(creator_id=current_user.id)

    else:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

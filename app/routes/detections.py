import os
import shutil
from datetime import datetime

from fastapi import APIRouter, HTTPException, Form, UploadFile, Depends, status
from app.schemas import users as users_schemas
from app.crud import tracker_data as tracker_data_crud
import celery_worker

from sqlalchemy.orm import Session
from app.models.database import SyncSessionLocal
from app.crud import users as users_crud
from app.crud import detections as detections_crud
from app.schemas import detections as detections_schemas

from sqlalchemy import insert

router = APIRouter()


@router.post('/run_detection_with_xml')
async def run_detection_with_xml(video_file: UploadFile, xml_file: UploadFile, description: str = Form(default=None),
                                 current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    files_path = f'static/detection_files/detection_with_xml/{datetime.now().strftime("%Y-%m-%d")}/upload_files'

    if not os.path.isdir(files_path):
        os.makedirs(files_path)

    video_path = f'{files_path}/{video_file.filename}'
    xml_path = f'{files_path}/{xml_file.filename}'

    with open(video_path, 'wb') as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    with open(xml_path, 'wb') as buffer:
        shutil.copyfileobj(xml_file.file, buffer)

    # celery_worker.run_detection_with_xml.delay(video_path=video_path, xml_path=xml_path, creator_id=current_user.id,
    #                                            description=description)

    return HTTPException(status_code=status.HTTP_200_OK)


@router.post('/run_detection_with_tracker')
async def run_detection_with_tracker(video_file: UploadFile, video_start_datetime: datetime = Form(),
                                     description: str = Form(default=None),
                                     current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    files_path = f'static/detection_files/detection_with_tracker/{datetime.now().strftime("%Y-%m-%d")}/upload_files'

    # video_start_datetime = datetime.strptime(str(video_start_datetime), "%Y-%m-%d %H:%M:%S")
    # tracker_data = await tracker_data_crud.get_current_location(video_start_datetime)
    #
    if not os.path.isdir(files_path):
        os.makedirs(files_path)

    video_path = f'{files_path}/{video_file.filename}'

    with open(video_path, 'wb') as buffer:
        shutil.copyfileobj(video_file.file, buffer)

    # # video_start_datetime = datetime.strptime(str(video_start_datetime), "%Y-%m-%d %H:%M:%S")
    #
    # celery_worker.run_detection_with_tracker.delay(creator_id=current_user.id, video_path=video_path,
    #                                                video_start_datetime=video_start_datetime, description=description)

    return HTTPException(status_code=status.HTTP_200_OK)


@router.get('/get_all_detections', response_model=list[detections_schemas.DetectionsWithUserName])
async def get_all_detections(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await detections_crud.get_all_detections_for_creator(creator_id=current_user.id)

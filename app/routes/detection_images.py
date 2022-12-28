from fastapi import APIRouter, Form

from app.crud import detection_images as detection_images_crud
from app.schemas import detection_images as detection_images_schemas

router = APIRouter()


@router.get('/get_detection_images', response_model=list[detection_images_schemas.DetectionImages])
async def get_detection_images(detection_id: int):
    return await detection_images_crud.get_detection_images(detection_id=detection_id)

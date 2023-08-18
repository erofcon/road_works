from fastapi import APIRouter, Form, Depends, HTTPException, status

from app.crud import user as users_crud
from app.crud import detection_images as detection_images_crud
from app.schemas import detection_images as detection_images_schemas
from app.schemas import user as users_schemas

router = APIRouter()


@router.get('/get_detection_images', response_model=list[detection_images_schemas.DetectionImages])
async def get_detection_images(detection_id: int,
                               current_user: users_schemas.UserWithCheckCreatorStatus = Depends(
                                   users_crud.get_current_user)):
    if not current_user.is_creator:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

    return await detection_images_crud.get_detection_images(detection_id=detection_id)


@router.post('/delete_detection_images')
async def delete_detection_images(detection_image_id: int = Form(),
                                  current_user: users_schemas.UserWithCheckCreatorStatus = Depends(
                                      users_crud.get_current_user)):

    if not current_user.is_creator:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    await detection_images_crud.delete_detection_images(detection_image_id=detection_image_id)
    return HTTPException(status_code=status.HTTP_204_NO_CONTENT)

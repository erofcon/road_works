from fastapi import APIRouter, HTTPException, Depends, status

from app.crud import user as user_crud
from app.crud import car as car_crud
from app.schemas import user as user_schemas

router = APIRouter()


@router.get('/get_all_cars')
async def get_all_cars(current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    if current_user.is_admin or current_user.is_creator:
        return await car_crud.get_all_cars()

    return HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)

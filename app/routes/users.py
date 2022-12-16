from fastapi import APIRouter, HTTPException, Depends, status

from app.crud import users as users_crud
from app.schemas import users as users_schemas

router = APIRouter()


@router.post('/create_user')
async def create_user(user: users_schemas.CreateUser):
    if await users_crud.get_user_by_name(user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User exists')

    if not await users_crud.create_user(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/related_user', response_model=list[users_schemas.User])
async def get_related_user(group_id: int, current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await users_crud.get_related_users(group_id=group_id)

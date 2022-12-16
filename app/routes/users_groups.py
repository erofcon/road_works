from fastapi import APIRouter, HTTPException, status

from app.crud import users_groups as users_groups_crud
from app.schemas import users_groups as users_groups_schemas

router = APIRouter()


@router.post('/create_related_users_groups')
async def create_related_users_groups(users_groups: users_groups_schemas.UsersGroupsBaseCreate):
    if not await users_groups_crud.create_related_users_groups(users_groups=users_groups):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)

from fastapi import APIRouter, HTTPException, Depends, status

from app.crud import users as users_crud
from app.crud import groups as groups_crud
from app.schemas import users as users_schemas
from app.schemas import groups as groups_schemas

router = APIRouter()


@router.post('/create_group')
async def create_group(group: groups_schemas.GroupsCreate):
    if await groups_crud.get_group_by_name(group.name):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Groups exists')

    if not await groups_crud.create_group(group=group):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/related_groups', response_model=list[groups_schemas.Groups])
async def get_related_groups(current_user: users_schemas.UsersBase = Depends(users_crud.get_current_user)):
    return await groups_crud.get_related_groups(user_id=current_user.id)

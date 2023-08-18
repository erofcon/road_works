from fastapi import APIRouter, HTTPException, Depends, status

from app.crud import user as user_crud
from app.crud import group as group_crud
from app.schemas import user as user_schemas
from app.schemas import group as group_schemas

router = APIRouter()


@router.post('/create_group')
async def create_group(group: group_schemas.GroupCreate,
                       current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    """
      Only admin can create group!
    """

    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if await group_crud.get_group_by_name(group.name):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Groups exists')

    if not await group_crud.create_group(group=group):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)


@router.get('/related_groups', response_model=list[group_schemas.Group])
async def get_related_groups(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    return await group_crud.get_related_groups(user_id=current_user.id)

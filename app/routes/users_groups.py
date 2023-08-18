from fastapi import APIRouter, HTTPException, Depends, status

from app.crud import user as user_crud
from app.crud import users_groups as users_groups_crud
from app.schemas import users_groups as users_groups_schemas
from app.schemas import user as user_schemas

router = APIRouter()


@router.post('/create_related_users_groups')
async def create_related_users_groups(users_groups: users_groups_schemas.UsersGroupsBaseCreate,
                                      current_user: user_schemas.UserWithCheckCreatorStatus = Depends(
                                          user_crud.get_current_user)):
    """
    Only admin can create users_groups!
    """

    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if not await users_groups_crud.create_related_users_groups(users_groups=users_groups):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)

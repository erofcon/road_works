from fastapi import APIRouter, HTTPException, Depends, status


from app.crud import user as user_crud
from app.schemas import user as user_schemas

router = APIRouter()


@router.post('/create_user')
async def create_user(user: user_schemas.CreateUser):
    """
    Test!!!
    """

    if await user_crud.get_user_by_name(user.username):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User exists')

    if not await user_crud.create_user(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return HTTPException(status_code=status.HTTP_201_CREATED)






""" TEST! CAN DELETE  """
@router.get('/get_related_executor_users', response_model=list[user_schemas.User])
async def get_related_executor_users(group_id: int,
                                     current_user: user_schemas.UserWithCheckCreatorStatus = Depends(
                                         user_crud.get_current_user)):
    if not current_user.is_creator:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED)
    return await user_crud.get_related_executor_users(group_id=group_id)


@router.get('/get_all_related_users')
async def get_all_related_users(
        current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    return await user_crud.get_all_related_users(user_id=current_user.id)


@router.post('/change_password')
async def change_password(new_password: str,
                          current_user: user_schemas.UserWithCheckCreatorStatus = Depends(user_crud.get_current_user)):
    return await user_crud.change_user_password(user=current_user,
                                                new_password=new_password)



""" TEST! CAN DELETE  """
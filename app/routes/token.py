from fastapi import APIRouter, Depends, HTTPException, Form, status
from fastapi.security import OAuth2PasswordRequestForm

from app.crud import user as user_crud
from app.crud import token as token_crud
from app.schemas import token as token_schemas
from app.schemas import user as user_schemas

router = APIRouter()


@router.post('/token')
async def get_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_crud.authenticate_user(username=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"}, )

    return token_crud.create_access_token(
        data=token_schemas.TokenData(sub=user.username,
                                     user=user_schemas.UserWithCheckCreatorStatus.from_orm(user)).dict())


@router.post('/refresh')
async def refresh_token(token: str = Form(), username: str = Form()):
    return token_crud.create_refresh_token(token=token, username=username)

from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from asyncpg.exceptions import DataError
from sqlalchemy import text

from app.crud import token as token_crud
from app.models.database import database
from app.models import users as users_model
from app.schemas import users as users_schemas
from app.schemas import token as token_schemas

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def _verify_password(plan_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plan_password, hash=hashed_password)


def _get_password_hash(password: str):
    return pwd_context.hash(secret=password)


async def get_user_by_name(username: str) -> users_schemas.CreateUser | None:
    query = users_model.users.select().where(users_model.users.c.username == username)
    return await database.fetch_one(query=query)


async def create_user(user: users_schemas.CreateUser) -> int | bool:
    hash_password = _get_password_hash(user.password)

    query = users_model.users.insert().values(
        username=user.username,
        password=hash_password,
        name=user.name,
        surname=user.surname,
        phone_number=user.phone_number,
        email=user.email,
        is_super_user=user.is_super_user,
        is_admin=user.is_admin,
        create_datetime=datetime.now(),
        related_company=user.related_company
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False


async def authenticate_user(username: str, password: str) -> users_schemas.UsersBase | None:
    user = await get_user_by_name(username=username)

    if not user:
        return None

    if not _verify_password(plan_password=password, hashed_password=user.password):
        return None

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> users_schemas.UsersBase:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token=token, key=token_crud.ACCESS_TOKEN_SECRET_KEY, algorithms=[token_crud.ALGORITHM])
        username: str = payload.get('sub')

        if username is None:
            raise credentials_exception

        token_data = token_schemas.TokenUser(username=username)

    except jwt.JWTClaimsError:
        raise credentials_exception

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired',
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await get_user_by_name(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_related_executor_users(group_id: int) -> list[users_schemas.User]:
    query = text(f"""
        SELECT 
            u.id, u.username 
        FROM 
            groups g
        LEFT JOIN 
            users_groups ug
        ON 
            ug.group_id=g.id
        LEFT JOIN 
            users u
        ON 
            u.id=ug.user_id
        LEFT JOIN 
            companies c
        ON 
            u.related_company=c.id
        WHERE 
            g.id={group_id} 
        AND 
            c.is_creator=false
    """)

    return await database.fetch_all(query=query)

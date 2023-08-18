from datetime import datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy import text

from app.crud import token as token_crud
from app.models.database import database
from app.models import user as user_model
from app.schemas import user as user_schemas
from app.schemas import token as token_schemas

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def _verify_password(plan_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(secret=plan_password, hash=hashed_password)


def _get_password_hash(password: str):
    return pwd_context.hash(secret=password)


async def get_user_by_name(username: str) -> user_schemas.CreateUser | None:
    query = user_model.user.select().where(user_model.user.c.username == username)
    return await database.fetch_one(query=query)


async def _get_user_by_name_for_token(username: str) -> user_schemas.UserWithCheckCreatorStatusAndPassword | None:
    query = text(f"""
                SELECT u.id, u.username, u.name, u.surname, u.password, u.email, u.is_admin, 
                c.is_creator
                FROM "user" u
                LEFT JOIN "company" c
                ON u.related_company = c.id
                WHERE u.username = '{username}'
    """)

    return await database.fetch_one(query=query)


async def create_user(user: user_schemas.CreateUser) -> int | bool:
    hash_password = _get_password_hash(user.password)

    query = user_model.user.insert().values(
        username=user.username,
        password=hash_password,
        name=user.name,
        surname=user.surname,
        phone_number=user.phone_number,
        email=user.email,
        is_admin=user.is_admin,
        create_datetime=datetime.now(),
        related_company=user.related_company
    )

    try:
        return await database.execute(query=query)
    except Exception:
        return False


async def change_user_password(user: user_schemas.UserWithCheckCreatorStatus, new_password: str):
    hash_password = _get_password_hash(new_password)

    query = text(f"""
        UPDATE 
            "user"
        SET password = '{hash_password}'
        WHERE id={user.id}
    """)

    return await database.execute(query=query)


async def authenticate_user(username: str, password: str) -> user_schemas.UserWithCheckCreatorStatus | None:
    user = await _get_user_by_name_for_token(username=username)

    if not user:
        return None

    if not _verify_password(plan_password=password, hashed_password=user.password):
        return None

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)) -> user_schemas.UserWithCheckCreatorStatus:
    """
    :param token:
    :return: model UserWithCheckCreatorStatus
    """

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

    user = await _get_user_by_name_for_token(username=token_data.username)
    if user is None:
        raise credentials_exception

    return user


async def get_related_executor_users(group_id: int) -> list[user_schemas.User]:
    query = text(f"""
        SELECT 
            u.id, u.username 
        FROM 
            "group" g
        LEFT JOIN 
            "users_groups" ug
        ON 
            ug.group_id=g.id
        LEFT JOIN 
            "user" u
        ON 
            u.id=ug.user_id
        LEFT JOIN 
            "company" c
        ON 
            u.related_company=c.id
        WHERE 
            g.id={group_id} 
        AND 
            c.is_creator=false
    """)

    return await database.fetch_all(query=query)


async def get_all_related_users(user_id: int):
    query = text(f"""
            SELECT 
                ur.id, ur.username, ur.name, ur.surname, ur.is_admin, c.is_creator
            FROM
                "user" u
            LEFT JOIN 
                "users_groups" ug
            ON
                ug.user_id=u.id
            LEFT JOIN
                "group" g
            ON
                g.id = ug.group_id
            LEFT JOIN
                "users_groups" ugr
            ON
                ugr.group_id=g.id
            LEFT JOIN
                "user" ur
            ON
                ur.id=ugr.user_id
            LEFT JOIN
                "company" c
            ON
                c.id = ur.related_company
            WHERE 
                u.id={user_id}
            AND
                ur.id!={user_id}
    """)

    return await database.fetch_all(query=query)

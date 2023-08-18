import asyncio

from loguru import logger

from app.models.database import database
from app.crud import user as user_crud
from app.schemas import user as user_schemas


async def create_admin():
    if not database.is_connected:
        await database.connect()
    username = input("username: ")
    password = input("password: ")

    user = user_schemas.CreateUser(username=username, password=password, is_admin=True)

    if not await user_crud.get_user_by_name(username=username):
        r = await user_crud.create_user(user=user)
        if not r:
            logger.error(f'error create {user}')
        else:
            logger.success(f'success create {user}')
    else:
        logger.error(f'error create {user}. User exists')

    await database.disconnect()


if __name__ == '__main__':
    asyncio.run(create_admin())

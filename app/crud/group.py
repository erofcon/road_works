from datetime import datetime

from sqlalchemy import text
from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import group as group_model
from app.schemas import group as group_schemas


async def get_group_by_name(name: str) -> group_schemas.Group | None:
    query = group_model.group.select().where(group_model.group.c.name == name)
    return await database.fetch_one(query=query)


async def create_group(group: group_schemas.GroupCreate):
    query = group_model.group.insert().values(
        name=group.name,
        create_datetime=datetime.now()
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False


async def get_related_groups(user_id: int) -> list[group_schemas.Group]:
    query = text(f"""
        SELECT 
            gr.id, gr.name, gr.create_datetime 
        FROM 
            "user" u 
        INNER JOIN 
            users_groups ug 
        ON 
            ug.user_id = u.id
        LEFT JOIN
            "group" gr 
        ON 
            ug.group_id=gr.id
        WHERE 
            u.id={user_id}
    """)

    return await database.fetch_all(query=query)

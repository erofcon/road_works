from datetime import datetime

from sqlalchemy import text
from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import groups as groups_model
from app.schemas import groups as groups_schemas


async def get_group_by_name(name: str) -> groups_schemas.Groups | None:
    query = groups_model.groups.select().where(groups_model.groups.c.name == name)
    return await database.fetch_one(query=query)


async def create_group(group: groups_schemas.GroupsCreate):
    query = groups_model.groups.insert().values(
        name=group.name,
        create_datetime=datetime.now()
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False


async def get_related_groups(user_id: int) -> list[groups_schemas.Groups]:
    query = text(f"""
        SELECT 
            gr.id, gr.name, gr.create_datetime 
        FROM 
            users u 
        INNER JOIN 
            users_groups ug 
        ON 
            ug.user_id = u.id
        LEFT JOIN
            groups gr 
        ON 
            ug.group_id=gr.id
        WHERE 
            u.id={user_id}
    """)

    return await database.fetch_all(query=query)

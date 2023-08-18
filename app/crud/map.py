from sqlalchemy import text
from geojson import MultiPoint

from app.models.database import database
from app.models import user as users_model
from app.models import task as tasks_model


async def get_geo_json_done_tasks(user_id: int):
    query = text(f"""
                SELECT 
                    *
                FROM
                    "task" t
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                WHERE
                    t.latitude IS NOT NULL
                AND 
                    t.longitude IS NOT NULL 
                AND
                    ug.user_id={user_id}
                AND
                    t.is_done=True
                """)
    location = []

    tasks = await database.fetch_all(query=query)

    for task in tasks:
        location.append((task.longitude, task.latitude))

    gjs = MultiPoint(location, precision=20)

    return gjs


async def get_geo_json_done_tasks_for_admin():
    query = text(f"""
                SELECT 
                    *
                FROM
                    "task" t
                WHERE
                    t.latitude IS NOT NULL
                AND 
                    t.longitude IS NOT NULL 
                AND
                    t.is_done=True
                """)
    location = []

    tasks = await database.fetch_all(query=query)

    for task in tasks:
        location.append((task.longitude, task.latitude))

    gjs = MultiPoint(location, precision=20)

    return gjs


async def get_geo_json_expired_tasks(user_id: int):
    query = text(f"""
                SELECT 
                    *
                FROM
                    "task" t
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                WHERE
                    t.latitude IS NOT NULL
                AND 
                    t.longitude IS NOT NULL 
                AND
                    ug.user_id={user_id}
                AND
                    t.is_done=False
                AND
                    t.lead_datetime < CURRENT_DATE
                """)
    location = []

    tasks = await database.fetch_all(query=query)

    for task in tasks:
        location.append((task.longitude, task.latitude))

    gjs = MultiPoint(location, precision=20)

    return gjs


async def get_geo_json_expired_tasks_for_admin():
    query = text(f"""
                SELECT 
                    *
                FROM
                    "task" t
                WHERE
                    t.latitude IS NOT NULL
                AND 
                    t.longitude IS NOT NULL 
                AND
                    t.is_done=False
                AND
                    t.lead_datetime < CURRENT_DATE
                """)
    location = []

    tasks = await database.fetch_all(query=query)

    for task in tasks:
        location.append((task.longitude, task.latitude))

    gjs = MultiPoint(location, precision=20)

    return gjs


async def get_geo_json_current_tasks(user_id: int):
    query = text(f"""
                SELECT 
                    *
                FROM
                    "task" t
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                WHERE
                    t.latitude IS NOT NULL
                AND 
                    t.longitude IS NOT NULL 
                AND
                    ug.user_id={user_id}
                AND
                    t.is_done=False
                AND
                    t.lead_datetime > CURRENT_DATE
                """)
    location = []

    tasks = await database.fetch_all(query=query)

    for task in tasks:
        location.append((task.longitude, task.latitude))

    gjs = MultiPoint(location, precision=20)

    return gjs


async def get_geo_json_current_tasks_for_admin():
    query = text(f"""
                SELECT 
                    *
                FROM
                    "task" t
                WHERE
                    t.latitude IS NOT NULL
                AND 
                    t.longitude IS NOT NULL 
                AND
                    t.is_done=False
                AND
                    t.lead_datetime > CURRENT_DATE
                """)
    location = []

    tasks = await database.fetch_all(query=query)

    for task in tasks:
        location.append((task.longitude, task.latitude))

    gjs = MultiPoint(location, precision=20)

    return gjs

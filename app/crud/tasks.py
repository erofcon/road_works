from datetime import datetime

from sqlalchemy import text
from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import tasks as tasks_model
from app.schemas import tasks as tasks_schemas


async def create_task(task: tasks_schemas.CreateTask, creator_id: int) -> int | bool:
    query = tasks_model.tasks.insert().values(
        description=task.description,
        create_datetime=datetime.now(),
        lead_datetime=task.lead_datetime,
        latitude=task.latitude,
        longitude=task.longitude,
        is_done=False,
        creator_id=creator_id,
        executor_id=task.executor_id,
        group_id=task.group_id
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False


async def get_current_tasks(user_id: int) -> list[tasks_schemas.CurrentTasks]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.lead_datetime, t.latitude, t.longitude,t.creator_id, t.executor_id,
        CASE 
            WHEN t.is_done=True 
            THEN 'is_done'
            WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
            THEN 'on_execution'
            WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
            THEN 'is_expired'
            ELSE 'unknown'
            END AS task_status
        FROM
            tasks t
        LEFT JOIN
            users_groups ug
        ON
            t.group_id=ug.group_id 
        WHERE 
            ug.user_id={user_id}
        AND
            t.is_done=False
        AND
            t.lead_datetime < CURRENT_DATE
    """)

    return await database.fetch_all(query=query)


async def get_expired_tasks(user_id: int) -> list[tasks_schemas.CurrentTasks]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.lead_datetime, t.latitude, t.longitude,t.creator_id, t.executor_id,
        CASE 
            WHEN t.is_done=True 
            THEN 'is_done'
            WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
            THEN 'on_execution'
            WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
            THEN 'is_expired'
            ELSE 'unknown'
            END AS task_status
        FROM
            tasks t
        LEFT JOIN
            users_groups ug
        ON
            t.group_id=ug.group_id 
        WHERE 
            ug.user_id={user_id}
        AND
            t.is_done=False
        AND
            t.lead_datetime > CURRENT_DATE
    """)

    return await database.fetch_all(query=query)


async def get_all_tasks(user_id: int) -> list[tasks_schemas.CurrentTasks]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.lead_datetime, t.latitude, t.longitude,t.creator_id, t.executor_id,
        CASE 
            WHEN t.is_done=True 
            THEN 'is_done'
            WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
            THEN 'on_execution'
            WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
            THEN 'is_expired'
            ELSE 'unknown'
            END AS task_status
    
        FROM
            tasks t
        LEFT JOIN
            users_groups ug
        ON
            t.group_id=ug.group_id 
        WHERE 
            ug.user_id={user_id}
    """)

    return await database.fetch_all(query=query)

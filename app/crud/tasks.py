from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import text
from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import tasks as tasks_model
from app.schemas import tasks as tasks_schemas
from app.schemas import users as users_schemas


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
            WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
            THEN 'on_execution'
            WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
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
            WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
            THEN 'on_execution'
            WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
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
            WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
            THEN 'on_execution'
            WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
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


async def get_base_task(task_id: int) -> tasks_schemas.Tasks:
    query = tasks_model.tasks.select().where(tasks_model.tasks.c.id == task_id)
    return await database.fetch_one(query=query)


async def get_task(task_id: int, current_user: users_schemas.UsersBase):
    task_query = f"""
            SELECT 
                t.id, t.description, t.create_datetime, 
                t.lead_datetime, t.latitude, t.longitude, g.id as group_id, g.name as group_name, t.creator_id, t.executor_id,
            CASE 
                WHEN t.is_done=True 
                THEN 'is_done'
                WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
                THEN 'on_execution'
                WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
            THEN 'is_expired'
                ELSE 'unknown'
                END AS task_status
            FROM
                tasks t
            LEFT JOIN groups g
            ON g.id=t.group_id
            WHERE 
                t.id={task_id}
    """

    task = await database.fetch_one(query=task_query)

    if not current_user.is_super_user and \
            not task.creator_id == current_user.id and not task.executor_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Permission denied'
        )

    task_images_query = f"""
                SELECT *
                FROM tasks_images ti
                WHERE ti.task_id={task.id}
    
    """

    task_creator_query = f"""
                    SELECT *
                    FROM users u
                    WHERE u.id={task.creator_id}

    """

    task_executor_query = f"""
                        SELECT *
                        FROM users u
                        WHERE u.id={task.executor_id}

    """

    task_images = await database.fetch_all(query=task_images_query)
    task_creator = await database.fetch_one(query=task_creator_query)
    task_executor = await database.fetch_one(query=task_executor_query)

    task_query = tasks_schemas.TaskQuery(**task)
    task_query.task_images = task_images
    task_query.task_creator = users_schemas.UsersBase(**task_creator)
    task_query.task_executor = users_schemas.UsersBase(**task_executor)

    return task_query


async def close_task(task_id: int):
    query = tasks_model.tasks.update().where(tasks_model.tasks.c.id == task_id).values(
        is_done=True
    )

    return await database.execute(query=query)

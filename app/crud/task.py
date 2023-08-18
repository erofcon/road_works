from datetime import datetime

from sqlalchemy import text
from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import task as task_model
from app.schemas import task as task_schemas
from app.schemas import user as user_schemas


async def create_task(task: task_schemas.CreateTask, creator_id: int) -> int | bool:
    query = task_model.task.insert().values(
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


async def get_current_tasks(user_id: int) -> list[task_schemas.CurrentTask]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.creator_id, t.executor_id,
            uc.username as creator_username,
            ue.username as executor_username,
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
            "task" t
        LEFT JOIN
            "users_groups" ug
        ON
            t.group_id=ug.group_id 
        LEFT JOIN "user" uc
        ON uc.id = t.creator_id
        LEFT JOIN "user" ue
        ON ue.id=t.executor_id
        WHERE 
            ug.user_id={user_id}
        AND
            t.is_done=False
        AND
            t.lead_datetime > CURRENT_DATE
        ORDER BY t.create_datetime DESC
    """)

    return await database.fetch_all(query=query)


async def get_current_tasks_for_admin() -> list[task_schemas.CurrentTask]:
    query = text("""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.creator_id, t.executor_id,
            uc.username as creator_username,
            ue.username as executor_username,
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
            "task" t
      
        LEFT JOIN "user" uc
        ON uc.id = t.creator_id
        LEFT JOIN "user" ue
        ON ue.id=t.executor_id
        WHERE 
            t.is_done=False
        AND
            t.lead_datetime > CURRENT_DATE
        ORDER BY t.create_datetime DESC
    """)

    return await database.fetch_all(query=query)


async def get_expired_tasks(user_id: int) -> list[task_schemas.CurrentTask]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.creator_id, t.executor_id,
            uc.username as creator_username,
            ue.username as executor_username,
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
            "task" t
        LEFT JOIN
            "users_groups" ug
        ON
            t.group_id=ug.group_id 
        LEFT JOIN "user" uc
        ON uc.id = t.creator_id
        LEFT JOIN "user" ue
        ON ue.id=t.executor_id
        WHERE 
            ug.user_id={user_id}
        AND
            t.is_done=False
        AND
            t.lead_datetime < CURRENT_DATE
            
        ORDER BY t.create_datetime DESC
    """)

    return await database.fetch_all(query=query)


async def get_expired_tasks_for_admin() -> list[task_schemas.CurrentTask]:
    query = text(f"""
            SELECT 
                t.id, t.description, t.create_datetime, 
                t.creator_id, t.executor_id,
                uc.username as creator_username,
                ue.username as executor_username,
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
                "task" t
                
            LEFT JOIN "user" uc
            ON uc.id = t.creator_id
            LEFT JOIN "user" ue
            ON ue.id=t.executor_id
            WHERE 
                t.is_done=False
            AND
                t.lead_datetime < CURRENT_DATE

            ORDER BY t.create_datetime DESC
        """)

    return await database.fetch_all(query=query)


async def get_done_tasks(user_id: int) -> list[task_schemas.CurrentTask]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.creator_id, t.executor_id,
            uc.username as creator_username,
            ue.username as executor_username,
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
            "task" t
        LEFT JOIN
            users_groups ug
        ON
            t.group_id=ug.group_id 
        LEFT JOIN "user" uc
        ON uc.id = t.creator_id
        LEFT JOIN "user" ue
        ON ue.id=t.executor_id
        WHERE 
            ug.user_id={user_id}
        AND
            t.is_done=True

        ORDER BY t.create_datetime DESC
    """)

    return await database.fetch_all(query=query)


async def get_done_tasks_for_admin() -> list[task_schemas.CurrentTask]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.creator_id, t.executor_id,
            uc.username as creator_username,
            ue.username as executor_username,
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
            "task" t
        
        LEFT JOIN "user" uc
        ON uc.id = t.creator_id
        LEFT JOIN "user" ue
        ON ue.id=t.executor_id
        WHERE t.is_done=True

        ORDER BY t.create_datetime DESC
    """)

    return await database.fetch_all(query=query)


async def get_all_tasks(user_id: int) -> list[task_schemas.CurrentTask]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.creator_id, t.executor_id,
            uc.username as creator_username,
            ue.username as executor_username,
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
            "task" t
        LEFT JOIN
            users_groups ug
        ON
            t.group_id=ug.group_id 
        LEFT JOIN "user" uc
        ON uc.id = t.creator_id
        LEFT JOIN "user" ue
        ON ue.id=t.executor_id
        WHERE 
            ug.user_id={user_id}
        ORDER BY t.create_datetime DESC
    """)

    return await database.fetch_all(query=query)


async def get_all_tasks_for_admin() -> list[task_schemas.CurrentTask]:
    query = text(f"""
        SELECT 
            t.id, t.description, t.create_datetime, 
            t.creator_id, t.executor_id,
            uc.username as creator_username,
            ue.username as executor_username,
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
            "task" t
        LEFT JOIN "user" uc
        ON uc.id = t.creator_id
        LEFT JOIN "user" ue
        ON ue.id=t.executor_id
        ORDER BY t.create_datetime DESC
    """)

    return await database.fetch_all(query=query)


async def get_base_task(task_id: int) -> task_schemas.Task:
    query = task_model.task.select().where(task_model.task.c.id == task_id)
    return await database.fetch_one(query=query)


async def get_task(task_id: int, current_user: user_schemas.UserWithCheckCreatorStatus):
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
                "task" t
            LEFT JOIN
                "users_groups" ug
            ON
                t.group_id=ug.group_id 
    
            LEFT JOIN 
                "group" g
            ON 
                g.id=t.group_id
            WHERE 
                t.id={task_id}
            """

    task = await database.fetch_one(query=task_query)

    task_images_query = f"""
                SELECT *
                FROM "task_images" ti
                WHERE ti.task_id={task.id}
    
    """

    task_creator_query = f"""
                    SELECT *
                    FROM "user" u
                    WHERE u.id={task.creator_id}

    """

    task_executor_query = f"""
                        SELECT *
                        FROM "user" u
                        WHERE u.id={task.executor_id}

    """

    task_images = await database.fetch_all(query=task_images_query)
    task_creator = await database.fetch_one(query=task_creator_query)
    task_executor = await database.fetch_one(query=task_executor_query)

    task_query = task_schemas.TaskQuery(**task)
    task_query.task_images = task_images
    task_query.task_creator = user_schemas.UserBase(**task_creator)
    task_query.task_executor = user_schemas.UserBase(**task_executor)

    return task_query


async def close_task(task_id: int):
    query = task_model.task.update().where(task_model.task.c.id == task_id).values(
        is_done=True
    )

    return await database.execute(query=query)


async def get_task_with_location(user_id: int, latitude: float, longitude: float):
    query = text(f"""
                SELECT 
                    t.id, t.description, t.creator_id, t.create_datetime, t.executor_id, uc.username as creator_username, 
                    ue.username as executor_username, ti.url,
                CASE 
                    WHEN t.is_done=True 
                    THEN 'is_done'
                    WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
                    THEN 'on_execution'
                    WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
                    THEN 'is_expired'
                    ELSE 'unknown'
                    END AS task_status
                FROM "task" t
                LEFT JOIN LATERAL
                    ( 
                     SELECT *
                     FROM "task_images" ti
                     WHERE ti.task_id = t.id
                     LIMIT 1
                    ) ti
                ON 
                    true
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                LEFT JOIN 
                    "user" uc
                ON 
                    uc.id = t.creator_id
                LEFT JOIN 
                    "user" ue
                ON 
                    ue.id=t.executor_id
                WHERE
                    ug.user_id={user_id}  
                AND
                    t.latitude = {latitude}
                AND 
                    t.longitude = {longitude}
    """)

    return await database.fetch_all(query=query)


async def get_task_with_location_for_admin(latitude: float, longitude: float):
    query = text(f"""
                SELECT 
                    t.id, t.description, t.creator_id, t.create_datetime, t.executor_id, uc.username as creator_username, 
                    ue.username as executor_username, ti.url,
                CASE 
                    WHEN t.is_done=True 
                    THEN 'is_done'
                    WHEN t.is_done=False and t.lead_datetime > CURRENT_DATE
                    THEN 'on_execution'
                    WHEN t.is_done=False and t.lead_datetime < CURRENT_DATE
                    THEN 'is_expired'
                    ELSE 'unknown'
                    END AS task_status
                FROM "task" t
                LEFT JOIN LATERAL
                    ( 
                     SELECT *
                     FROM "task_images" ti
                     WHERE ti.task_id = t.id
                     LIMIT 1
                    ) ti
                ON 
                    true
                    
                LEFT JOIN 
                    "user" uc
                ON 
                    uc.id = t.creator_id
                LEFT JOIN 
                    "user" ue
                ON 
                    ue.id=t.executor_id
                WHERE
                    t.latitude = {latitude}
                AND 
                    t.longitude = {longitude}
    """)

    return await database.fetch_all(query=query)


async def get_last_current_task_with_image(user_id: int):
    query = text(f"""
                SELECT 
                    t.id, t.description, ti.url
                FROM 
                    "task" t
                LEFT JOIN 
                    "users_groups" ug
                ON 
                    ug.group_id = t.group_id
                LEFT JOIN LATERAL
                    (
                        SELECT *
                        FROM "task_images" ti
                        WHERE ti.task_id = t.id
                        LIMIT 1
                    ) ti
                ON 
                    true
                WHERE 
                    ug.user_id={user_id}
                AND
                    t.is_done=False
                AND
                    t.lead_datetime > CURRENT_DATE
                ORDER BY 
                    t.create_datetime DESC
                LIMIT 1

    """)

    return await database.fetch_one(query=query)


async def get_last_current_task_with_image_for_admin():
    query = text("""
                SELECT 
                    t.id, t.description, ti.url
                FROM 
                    "task" t
                LEFT JOIN LATERAL
                    (
                        SELECT *
                        FROM "task_images" ti
                        WHERE ti.task_id = t.id
                        LIMIT 1
                    ) ti
                ON 
                    true
                WHERE 
                    t.is_done=False
                AND
                    t.lead_datetime > CURRENT_DATE
                ORDER BY 
                    t.create_datetime DESC
                LIMIT 1

    """)

    return await database.fetch_one(query=query)


async def get_task_statistic_for_user(user_id: int):
    query = text(f"""
        SELECT
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                WHERE 
                    t.is_done=True
                AND
                    ug.user_id={user_id}
            ) as done_tasks,
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                WHERE 
                    t.is_done=False
                AND
                    t.lead_datetime < CURRENT_DATE
                AND
                    ug.user_id={user_id}
            ) as expired_tasks,
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                WHERE 
                    t.is_done=False
                AND
                    t.lead_datetime > CURRENT_DATE
                AND
                    ug.user_id={user_id}
            ) as current_tasks,
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
                LEFT JOIN
                    "users_groups" ug
                ON
                    t.group_id=ug.group_id 
                WHERE
                    ug.user_id={user_id}
            ) as all_tasks
    """)

    return await database.fetch_one(query=query)


async def get_task_statistic_for_admin():
    query = text(f"""
        SELECT
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
                WHERE 
                    t.is_done=True
            ) as done_tasks,
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
                
                WHERE 
                    t.is_done=False
                AND
                    t.lead_datetime < CURRENT_DATE
            ) as expired_tasks,
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
                WHERE 
                    t.is_done=False
                AND
                    t.lead_datetime > CURRENT_DATE
            ) as current_tasks,
            (
                SELECT 
                    COUNT(*)
                FROM 
                    "task" t
            ) as all_tasks
    """)

    return await database.fetch_one(query=query)

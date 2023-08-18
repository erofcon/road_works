from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import task_images as task_images_models
from app.schemas import task_images as task_images_schemas


async def create_task_images(task: task_images_schemas.TaskImagesCreate):
    query = task_images_models.task_images.insert().values(
        url=task.url,
        task_id=task.task_id
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False

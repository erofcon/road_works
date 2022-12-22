from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import detection_images as detection_images_model
from app.schemas import detection_images as detection_images_schemas


async def create_detection_images(detection_images: detection_images_schemas.DetectionImagesCreate,
                                  detection_id: int) -> int | bool:
    query = detection_images_model.detection_images.insert().values(
        url=detection_images.url,
        latitude=detection_images.latitude,
        longitude=detection_images.longitude,
        detection_id=detection_id
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False

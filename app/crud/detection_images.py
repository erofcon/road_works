from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from app.models.database import database
from app.models import detection_images as detection_images_model
from app.schemas import detection_images as detection_images_schemas


def create_detection_images(detection_images: detection_images_schemas.DetectionImagesCreate,
                            detection_id: int, db: Session) -> int | bool:
    query = detection_images_model.detection_images.insert().values(
        url=detection_images.url,
        latitude=detection_images.latitude,
        longitude=detection_images.longitude,
        detection_id=detection_id
    )

    try:
        model = db.execute(query)
        db.commit()
        return model.inserted_primary_key
    except DataError:
        db.rollback()
        return False


async def get_detection_images(detection_id: int) -> list[detection_images_schemas.DetectionImages]:
    query = detection_images_model.detection_images.select().where(
        detection_images_model.detection_images.c.detection_id == detection_id)

    return await database.fetch_all(query=query)


async def delete_detection_images(detection_image_id: int) -> bool:
    query = detection_images_model.detection_images.delete().where(
        detection_images_model.detection_images.c.id == detection_image_id)

    return await database.execute(query=query)

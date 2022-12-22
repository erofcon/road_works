from datetime import datetime

from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import detections as detections_model
from app.schemas import detections as detections_schemas


async def create_detection(detection: detections_schemas.DetectionsCreate) -> int | bool:
    query = detections_model.detections.insert().values(
        descriptions=detection.description,
        create_datetime=datetime.now(),
        creator_id=detection.creator_id
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False

from sqlalchemy import text
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from app.models.database import database
from app.models import detection_locations as detection_locations_models
from app.schemas import detection_locations as detection_locations_schemas


def create_detection(detection_locations: detection_locations_schemas.DetectionLocationsBase, detection_id: int,
                     db: Session) -> int | bool:
    query = detection_locations_models.detection_locations.insert().values(
        latitude=detection_locations.latitude,
        longitude=detection_locations.longitude,
        detection_id=detection_id
    )

    try:
        model = db.execute(query)
        db.commit()
        return model.inserted_primary_key[0]
    except DataError:
        return False


async def get_detection_locations(detection_id: int):
    query = text(f"""
        SELECT 
            *
        FROM
            detection_locations
        WHERE 
            detection_id={detection_id}
    """)

    return await database.fetch_all(query=query)

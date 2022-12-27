from datetime import datetime

from sqlalchemy import text
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

from app.models.database import database
from app.models import detections as detections_model
from app.schemas import detections as detections_schemas


def create_detection(detection: detections_schemas.DetectionsCreate, db: Session) -> int | bool:
    query = detections_model.detections.insert().values(
        descriptions=detection.description,
        create_datetime=datetime.now(),
        creator_id=detection.creator_id
    )

    try:
        model = db.execute(query)
        db.commit()
        return model.inserted_primary_key[0]
    except DataError:
        return False


async def get_all_detections_for_creator(creator_id: int) -> list[detections_schemas.DetectionsWithUserName]:
    query = text(f"""
        SELECT d.id,d.descriptions,d.create_datetime, d.creator_id, u.username
        FROM detections d
        LEFT JOIN users u
        ON u.id=d.creator_id
        WHERE d.creator_id={creator_id}
    """)

    return await database.fetch_all(query=query)

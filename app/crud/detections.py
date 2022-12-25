from datetime import datetime

from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session

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



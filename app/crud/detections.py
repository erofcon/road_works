from datetime import datetime

from sqlalchemy.orm import Session

from app.models import detections as detections_model
from app.schemas import detections as detections_schemas


def create_detection(detection: detections_schemas.DetectionsCreate, db: Session) -> int | bool:
    query = detections_model.detections.insert().values(
        descriptions=detection.description,
        create_datetime=datetime.now(),
        creator_id=detection.creator_id
    )

    db.add(query)
    db.commit()
    db.refresh(query)

    print(query)

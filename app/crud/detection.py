from datetime import datetime

from sqlalchemy import text
from sqlalchemy.exc import DataError
from sqlalchemy.orm import Session
from geojson import MultiPoint

from app.models.database import database
from app.models import detection as detection_model
from app.crud import detection_locations as detection_locations_crud
from app.schemas import detection as detection_schemas


def create_detection(detection: detection_schemas.DetectionCreate, db: Session) -> int:
    query = detection_model.detection.insert().values(
        descriptions=detection.descriptions,
        create_datetime=datetime.now(),
        creator_id=detection.creator_id
    )

    # try:
    model = db.execute(query)
    db.commit()
    return model.inserted_primary_key[0]
    # except DataError:
    #     return False


async def get_all_detections_for_creator(creator_id: int) -> list[detection_schemas.DetectionWithUserName]:
    query = text(f"""
        SELECT d.id,d.descriptions,d.create_datetime, d.creator_id, u.username, COUNT(di.id) as detection_image_count
        FROM "detection" d
        LEFT JOIN "user" u
        ON u.id=d.creator_id
        LEFT JOIN "detection_images" di
        ON di.detection_id = d.id
        WHERE d.creator_id={creator_id}
        GROUP BY d.id, u.username
    """)

    return await database.fetch_all(query=query)


async def get_all_detections_for_admin() -> list[detection_schemas.DetectionWithUserName]:
    query = text(f"""
        SELECT d.id,d.descriptions,d.create_datetime, d.creator_id, u.username, COUNT(di.id) as detection_image_count
        FROM "detection" d
        LEFT JOIN "user" u
        ON u.id=d.creator_id
        LEFT JOIN "detection_images" di
        ON di.detection_id = d.id
        GROUP BY d.id, u.username
    """)

    return await database.fetch_all(query=query)


async def get_all_detection_for_groups_users(creator_id: int) -> detection_schemas.Detection:
    query = text(f"""
            SELECT 
                d.id, d.descriptions, d.create_datetime, d.creator_id
            FROM
                "user" u
            LEFT JOIN 
                "users_groups" ug
            ON
                ug.user_id=u.id
            LEFT JOIN
                "group" g
            ON
                g.id = ug.group_id
            LEFT JOIN
                "users_groups" ugr
            ON
                ugr.group_id=g.id
            LEFT JOIN
                "user" ur
            ON
                ur.id=ugr.user_id
            RIGHT JOIN 
                "detection" d
            ON
                d.creator_id = ur.id
            WHERE 
                u.id={creator_id}
    """)

    return await database.fetch_all(query=query)


async def get_all_detection_with_locations_for_groups_users(creator_id: int):
    return_detections = []

    detections = await get_all_detection_for_groups_users(creator_id=creator_id)

    for detection in detections:
        one_detection = detection_schemas.DetectionWithLocations(**detection)
        locations = await detection_locations_crud.get_detection_locations(detection_id=detection.id)
        location = []

        for loc in locations:
            location.append((loc.latitude, loc.longitude))

        gjs = MultiPoint(location, precision=20)

        one_detection.locations = gjs

        return_detections.append(one_detection)

    return return_detections

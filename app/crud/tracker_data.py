import math
from datetime import datetime

from sqlalchemy import text

from app.models.database import database
from app.schemas import tracker_data as tracker_data_schemas


async def get_current_location(time: datetime) -> tracker_data_schemas.TrackerData:
    query_gt = text(f"""
        SELECT * 
        FROM tracker_data tr 
        WHERE tr.create_datetime >= '{time}'
        ORDER BY tr.create_datetime
        LIMIT 1
        """)

    query_lt = text(f"""
        SELECT * 
        FROM tracker_data tr 
        WHERE tr.create_datetime <= '{time}'
        ORDER BY tr.create_datetime DESC
        LIMIT 1
    """)

    gt_fetch = await database.fetch_one(query_gt)
    lt_fetch = await database.fetch_one(query_lt)

    gt_diff = (gt_fetch.create_datetime - time).total_seconds() if gt_fetch else math.inf
    lt_diff = (time - lt_fetch.create_datetime).total_seconds() if lt_fetch else math.inf

    return gt_fetch if gt_diff <= lt_diff else lt_fetch

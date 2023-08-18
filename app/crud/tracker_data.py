import math
from datetime import datetime
from typing import List

from sqlalchemy import text
from sqlalchemy.engine import Result, Row
from sqlalchemy.orm import Session


def get_current_location(time: datetime, db: Session) -> Row | None:
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

    db.rollback()

    gt_fetch = db.execute(query_gt)
    lt_fetch = db.execute(query_lt)

    gt_fetch = gt_fetch.fetchone()
    lt_fetch = lt_fetch.fetchone()

    gt_diff = (gt_fetch[3] - time).total_seconds() if gt_fetch else math.inf
    lt_diff = (time - lt_fetch[3]).total_seconds() if lt_fetch else math.inf

    return gt_fetch if gt_diff <= lt_diff else lt_fetch


def get_location_between_data(start_datetime: str, end_datetime: str, db: Session) -> list[Row]:
    query = text(f"""
           SELECT latitude, longitude
            FROM tracker_data td
            WHERE td.create_datetime
            BETWEEN '{start_datetime}'
            AND '{end_datetime}'
            """)

    db.rollback()

    query_exec = db.execute(query)
    return query_exec.fetchall()

    # try:
    #     query_exec = db.execute(query)
    #     return query_exec.fetchall()
    # except:
    #     db.rollback()
    #
    # return None

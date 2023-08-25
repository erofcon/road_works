from sqlalchemy import text

from app.models.database import database
from app.schemas import car as car_scheme


async def get_all_cars() -> list[car_scheme.Car]:
    query = text("""
        SELECT * FROM car
    """)

    return await database.fetch_all(query=query)

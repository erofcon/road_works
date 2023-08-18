from datetime import datetime

from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import company as companies_model
from app.schemas import company as companies_schemas


async def get_company_by_name(name: str) -> companies_schemas.Company | None:
    query = companies_model.company.select().where(companies_model.company.c.name == name)
    return await database.fetch_one(query=query)


async def create_company(company: companies_schemas.CompanyCreate):
    query = companies_model.company.insert().values(
        name=company.name,
        is_creator=company.is_creator,
        create_datetime=datetime.now()
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False

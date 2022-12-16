from datetime import datetime

from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import companies as companies_model
from app.schemas import companies as companies_schemas


async def get_company_by_name(name: str) -> companies_schemas.Companies | None:
    query = companies_model.companies.select().where(companies_model.companies.c.name == name)
    return await database.fetch_one(query=query)


async def create_company(company: companies_schemas.CompaniesCreate):
    query = companies_model.companies.insert().values(
        name=company.name,
        is_creator=company.is_creator,
        create_datetime=datetime.now()
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False

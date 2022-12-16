from asyncpg.exceptions import DataError

from app.models.database import database
from app.models import companies_groups as companies_groups_model
from app.schemas import companies_groups as companies_groups_schemas


async def create_related_companies_groups(companies_groups: companies_groups_schemas.CompaniesGroupsBaseCreate):
    query = companies_groups_model.companies_groups.insert().values(
        company_id=companies_groups.company_id,
        group_id=companies_groups.group_id
    )

    try:
        return await database.execute(query=query)
    except DataError:
        return False
